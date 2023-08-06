from fractions import Fraction
from math import sqrt, prod, log2, ceil
from typing import NamedTuple, Tuple, Optional, Iterable, List
from collections import Counter
from rfb_mc.implementation.eamp.eamp_rfm import EampRfm, get_cn, EampParams, EampTransformMethod, get_pj
from rfb_mc.implementation.eamp.utility import multi_majority_vote_iteration_count_to_ensure_beta, \
    majority_vote_error_probability
from rfb_mc.scheduler import SchedulerBase
from rfb_mc.store import StoreBase
from rfb_mc.types import RfBmcTask, RfBmcResult

EampEdgeInterval = NamedTuple("EampEdgeInterval", [
    ("interval", Tuple[int, int]),
    ("confidence", float),
])


class EampEdgeScheduler(SchedulerBase[EampEdgeInterval, EampEdgeInterval, EampRfm]):
    def __init__(
        self,
        store: StoreBase,
        confidence: Fraction,
        a: int,
        q: int,
        max_model_count: Optional[int] = None,
    ):
        super().__init__(store, EampRfm)

        assert a >= 1, "a >= 1"
        assert q >= 1, "q >= 1"
        assert 0 <= confidence < 1, "Confidence is < 1 and >= 0"

        self.confidence: Fraction = confidence
        self.a: int = a
        self.q: int = q
        self.max_model_count = max_model_count if max_model_count is not None else prod([
            (2 ** bit_width) ** count for bit_width, count in self.store.data.params.bit_width_counter.items()
        ])

    def _run_algorithm_once(self):
        g = (sqrt(self.a + 1) - 1) ** 2
        G = (sqrt(self.a + 1) + 1) ** 2

        cn = get_cn(self.max_model_count ** self.q, G)

        beta = 1 - self.confidence

        # maximum amount of k values that need to be iterated for c[0]
        max_k = max(int(ceil(max([
            log2(get_pj(i) / prod([get_pj(j) for j in range(1, i)]))
            for i in range(1, cn)
        ]))) - 1, 1) if cn > 1 else 1

        # maximum amount of expected majority vote counting procedures
        max_majority_vote_countings = cn - 1 + max_k

        # probability that an estimate call returns the less likely result
        alpha = Fraction(1, 4)

        r = multi_majority_vote_iteration_count_to_ensure_beta(
            alpha,
            beta,
            max_majority_vote_countings,
        )

        def make_eamp_params(c: Iterable[int]):
            return EampParams(
                c=tuple(c),
                transform_method=EampTransformMethod.SORTED_ROLLING_WINDOW,
            )

        def make_rf_bmc_task(eamp_params: EampParams):
            return RfBmcTask(
                rfm_guid=self.rf_module.get_guid(),
                rfm_formula_params=eamp_params,
                a=self.a,
                q=self.q,
            )

        def range_size(c: Iterable[int]):
            return self.rf_module.get_restrictive_formula_properties(
                self.store.data.params, make_eamp_params(c),
            ).range_size

        def pre_estimate(c: List[int]) -> Optional[bool]:
            max_mc = self.max_model_count ** self.q

            if max_mc < range_size(c) * G:
                return False
            elif range_size(c) == 0:
                return True
            elif c_neg is not None and range_size(c_neg) <= range_size(c):
                return False
            elif c_pos is not None and range_size(c) <= range_size(c_pos):
                return True
            else:
                return None

        # TODO: handle model count being too small

        c_pos: Optional[List[int]] = None

        c_neg: Optional[List[int]] = None

        # errors majority vote countings have introduced
        mv_error_probabilities: List[Fraction] = []

        def get_edge_interval():
            r_c_pos = range_size(c_pos) if c_pos is not None else None

            r_c_neg = range_size(c_neg) if c_neg is not None else None

            # TODO: investigate precision of q-th root
            return EampEdgeInterval(
                interval=(
                    (r_c_pos * g) ** (1 / self.q) if r_c_pos is not None else 0,
                    min(self.max_model_count, (r_c_neg * G) ** (1 / self.q))
                    if r_c_neg is not None else self.max_model_count
                ),
                # probability of error is lower than the sum of the majority vote counting error probabilities
                confidence=1.0 if len(mv_error_probabilities) == 0
                else float(1 - sum(mv_error_probabilities)),
            )

        def majority_vote_estimate(c: List[int]):
            while True:
                rf_bmc_task = make_rf_bmc_task(make_eamp_params(c))

                # copies the required results data in order for it not to be modified while using them
                rf_bmc_results: Counter[RfBmcResult] = \
                    self.store.data.rf_bmc_results_map.get(rf_bmc_task, Counter()).copy()

                positive_voters = sum([
                    count
                    for result, count in rf_bmc_results.items()
                    if result.bmc is None
                ])

                negative_voters = sum([
                    count
                    for result, count in rf_bmc_results.items()
                    if result.bmc is not None
                ])

                rr = max(0, r - (positive_voters + negative_voters))

                if positive_voters >= negative_voters and positive_voters >= negative_voters + rr:
                    return True, majority_vote_error_probability(alpha, positive_voters, negative_voters)

                if negative_voters > positive_voters and negative_voters > positive_voters + rr:
                    return False, majority_vote_error_probability(alpha, positive_voters, negative_voters)

                yield EampEdgeScheduler.AlgorithmYield(
                    required_tasks=Counter(rr * [rf_bmc_task]),
                    predicted_required_tasks=Counter(),
                    intermediate_result=get_edge_interval(),
                )

        c = [0] * (cn - 1) + [1]
        j = cn - 1

        while True:
            while pre_estimate(c) is False and j != 0:
                c_neg = c.copy()

                c[j] = 0
                c[j - 1] = 1
                j -= 1

            if pre_estimate(c) is False and j == 0:
                c_neg = c.copy()
                break

            mv_estimate, mv_error_prob = yield from majority_vote_estimate(c)
            mv_error_probabilities.append(mv_error_prob)

            if mv_estimate:
                c_pos = c.copy()

                if j == 0:
                    c[j] += 1
                else:
                    c[j - 1] = 1
                    j -= 1
            else:
                c_neg = c.copy()

                if j == 0:
                    break
                else:
                    c[j] = 0
                    c[j - 1] = 1
                    j -= 1

        return get_edge_interval()

    def _run_algorithm(self):
        yield from self._run_algorithm_once()
        # second iteration ensures updated results are used
        return (yield from self._run_algorithm_once())
