# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .base_recommender import AbstractRecommender
from itertools import groupby
from scipy.spatial import distance
from taar.logs.interfaces import IMozLogging
import numpy as np
from taar.recommenders.cache import TAARCache

import markus

metrics = markus.get_metrics("taar")

FLOOR_DISTANCE_ADJUSTMENT = 0.001

CATEGORICAL_FEATURES = ["geo_city", "locale", "os"]
CONTINUOUS_FEATURES = [
    "subsession_length",
    "bookmark_count",
    "tab_open_count",
    "total_uri",
    "unique_tlds",
]


class SimilarityRecommender(AbstractRecommender):
    """ A recommender class that returns top N addons based on the
    client similarity with a set of candidate addon donors.

    Several telemetry fields are used to compute pairwise similarity
    with the donors and similarities are converted into a likelihood
    ratio of being a good match versus not being a good match. These
    quantities are then used to rank specific addons for
    recommendation.

    This will load a json file containing updated list of addon donors
    updated periodically by a separate weekly process using
    Longitdudinal Telemetry data.

    This recommender may provide useful recommendations when
    collaborative_recommender may not work.
    """

    def __init__(self, ctx):
        self._ctx = ctx

        self._cache = self._ctx[TAARCache]

        self.logger = self._ctx[IMozLogging].get_logger("taar")

    def _get_cache(self, extra_data):
        tmp = extra_data.get("cache", None)
        if tmp is None:
            tmp = self._cache.cache_context()
        return tmp

    """
    End private properties
    """

    def can_recommend(self, client_data, extra_data={}):
        cache = self._get_cache(extra_data)
        # We can't recommend if we don't have our data files.
        if cache["donors_pool"] is None or cache["lr_curves"] is None:
            return False

        # Check that the client info contains a non-None value for each required
        # telemetry field.
        REQUIRED_FIELDS = CATEGORICAL_FEATURES + CONTINUOUS_FEATURES

        has_fields = all(
            [client_data.get(f, None) is not None for f in REQUIRED_FIELDS]
        )
        if not has_fields:
            # Can not add extra info because client_id may not be available.
            self.logger.error("Unusable client data encountered")
        return has_fields

    def get_lr(self, score, cache):
        """Compute a :float: likelihood ratio from a provided similarity score when compared
        to two probability density functions which are computed and pre-loaded during init.

        The numerator indicates the probability density that a particular similarity score
        corresponds to a 'good' addon donor, i.e. a client that is similar in the sense of
        telemetry variables. The denominator indicates the probability density that a particular
        similarity score corresponds to a 'poor' addon donor

        :param score: A similarity score between a pair of objects.
        :returns: The approximate float likelihood ratio corresponding to provided score.
        """
        # Find the index of the closest value that was precomputed in lr_curves
        # This will significantly speed up |get_lr|.

        # The lr_curves_cache is a list of scalar distance
        # measurements
        lr_curves_cache = np.array([s[0] for s in cache["lr_curves"]])

        # np.argmin produces the index to the part of the curve
        # where distance is the smallest to the score which we are
        # inspecting currently.
        idx = np.argmin(abs(score - lr_curves_cache))

        numer_val = cache["lr_curves"][idx][1][0]
        denum_val = cache["lr_curves"][idx][1][1]

        # Compute LR based on numerator and denominator values
        return float(numer_val) / float(denum_val)

    # # # CAUTION! # # #
    # Any changes to this function must be reflected in the corresponding ETL job.
    # https://github.com/mozilla/python_mozetl/blob/master/mozetl/taar/taar_similarity.py
    #
    def compute_clients_dist(self, client_data, cache):
        client_categorical_feats = [
            client_data.get(specified_key) for specified_key in CATEGORICAL_FEATURES
        ]
        client_continuous_feats = [
            client_data.get(specified_key) for specified_key in CONTINUOUS_FEATURES
        ]

        # Compute the distances between the user and the cached continuous features.
        cont_features = distance.cdist(
            cache["continuous_features"],
            np.array([client_continuous_feats]),
            "canberra",
        )

        # Compute the distances between the user and the cached categorical features.
        cat_features = np.array(
            [
                [distance.hamming(x, client_categorical_feats)]
                for x in cache["categorical_features"]
            ]
        )

        # See the "Note about cdist optimization" in README.md for why we only use cdist once.

        # Take the product of similarities to attain a univariate similarity score.
        # Note that the addition of 0.001 to the continuous features
        # sets a floor value to the distance in continuous similarity
        # scores.  There is no such floor value set for categorical
        # features so this adjustment prioritizes categorical
        # similarity over continous similarity
        return (cont_features + FLOOR_DISTANCE_ADJUSTMENT) * cat_features

    def get_similar_donors(self, client_data, cache):
        """Computes a set of :float: similarity scores between a client and a set of candidate
        donors for which comparable variables have been measured.

        A custom similarity metric is defined in this function that combines the Hamming distance
        for categorical variables with the Canberra distance for continuous variables into a
        univariate similarity metric between the client and a set of candidate donors loaded during
        init.

        :param client_data: a client data payload including a subset fo telemetry fields.
        :return: the sorted approximate likelihood ratio (np.array) corresponding to the
                 internally computed similarity score and a list of indices that link
                 each LR score with the related donor in the |self.donors_pool|.
        """
        # Compute the distance between self and any comparable client.
        distances = self.compute_clients_dist(client_data, cache)

        # Compute the LR based on precomputed distributions that relate the score
        # to a probability of providing good addon recommendations.

        lrs_from_scores = np.array(
            [self.get_lr(distances[i], cache) for i in range(cache["num_donors"])]
        )

        # Sort the LR values (descending) and return the sorted values together with
        # the original indices.
        indices = (-lrs_from_scores).argsort()
        return lrs_from_scores[indices], indices

    def _recommend(self, client_data, limit, extra_data={}):
        cache = self._get_cache(extra_data)

        donor_set_ranking, indices = self.get_similar_donors(client_data, cache)
        donor_log_lrs = np.log(donor_set_ranking)
        # 1.0 corresponds to a log likelihood ratio of 0 meaning that donors are equally
        # likely to be 'good'. A value > 0.0 is sufficient, but we like this to be high.
        if donor_log_lrs[0] < 0.1:
            self.logger.warning(
                "Addons recommended with very low similarity score, perhaps donor set is unrepresentative",
                extra={"maximum_similarity": donor_set_ranking[0]},
            )

        # Retrieve the indices of the highest ranked donors and then append their
        # installed addons.
        index_lrs_iter = zip(indices[donor_log_lrs > 0.0], donor_log_lrs)
        recommendations = []
        for (index, lrs) in index_lrs_iter:
            for term in cache["donors_pool"][index]["active_addons"]:
                candidate = (term, lrs)
                recommendations.append(candidate)
        # Sort recommendations on key (guid name)
        recommendations = sorted(recommendations, key=lambda x: x[0])
        recommendations_out = []
        # recommendations must be sorted for this to work.
        for guid_key, group in groupby(recommendations, key=lambda x: x[0]):
            recommendations_out.append((guid_key, sum(j for i, j in group)))
        # now re-sort on the basis of LLR.
        recommendations_out = sorted(recommendations_out, key=lambda x: -x[1])

        log_data = (
            client_data["client_id"],
            str([r[0] for r in recommendations_out[:limit]]),
        )
        self.logger.debug(
            "similarity_recommender_triggered, "
            "client_id: [%s], guids: [%s]" % log_data
        )
        return recommendations_out

    @metrics.timer_decorator("similarity_recommend")
    def recommend(self, client_data, limit, extra_data={}):
        try:
            recommendations_out = self._recommend(client_data, limit, extra_data)
        except Exception as e:
            recommendations_out = []

            metrics.incr("error_similarity", value=1)
            self.logger.exception(
                "Similarity recommender crashed for {}".format(
                    client_data.get("client_id", "no-client-id")
                ),
                e,
            )

        return recommendations_out[:limit]
