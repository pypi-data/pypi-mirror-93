from enum import Enum, unique
from math import prod, log2, floor
from typing import NamedTuple, Tuple, Any
from rfb_mc.implementation.eamp.primes import get_smallest_prime_above_or_equal_power_of_two, \
    get_highest_power_two_key_in_dict
from rfb_mc.restrictive_formula_module import RestrictiveFormulaModuleBase
from rfb_mc.runner import RunnerRandom
from rfb_mc.types import Params


@unique
class EampTransformMethod(Enum):
    SORTED_ROLLING_WINDOW = "SRW"


EampParams = NamedTuple("EampParams", [
    ("c", Tuple[int, ...]),
    ("transform_method", EampTransformMethod),
])

EampParamProperties = NamedTuple("EampParamProperties", [
    ("range_size", int),
])

EampInstanceParams = NamedTuple("EampInstanceParams", [
    ("params", EampParams),
    ("coefficients", Tuple[Tuple[Tuple[Tuple[int, ...], int, int], ...], ...]),
])


class EampRfm(RestrictiveFormulaModuleBase[EampParams, EampParamProperties, EampInstanceParams]):
    @classmethod
    def get_guid(cls):
        return "eamp-rfm"

    @classmethod
    def encode_restrictive_formula_params(
        cls,
        params: EampParams,
    ) -> Any:
        return (
            params.c,
            params.transform_method.value
        )

    @classmethod
    def decode_restrictive_formula_params(
        cls,
        params: Any,
    ) -> EampParams:
        c, transform_method = params

        return EampParams(
            c=c,
            transform_method=EampTransformMethod(transform_method)
        )

    @classmethod
    def get_restrictive_formula_properties(
        cls,
        params: Params,
        restrictive_formula_params: EampParams,
    ) -> EampParamProperties:
        return EampParamProperties(
            range_size=get_range_size(restrictive_formula_params.c)
        )

    @classmethod
    def generate_restrictive_formula_instance_params(
        cls,
        params: Params,
        restrictive_formula_params: EampParams,
        q: int,
        random: RunnerRandom,
    ) -> EampInstanceParams:
        variables = []

        for size in sorted(params.bit_width_counter.keys()):
            # add amount of variables with size q-times as they are cloned q-times
            variables += [size] * params.bit_width_counter[size] * q

        def get_slice_count_sorted_rolling_window(domain_bit_count: int) -> int:
            slice_count = 0

            queue = sorted(variables)

            while len(queue) > 0:
                x = queue.pop(0)

                if x >= domain_bit_count:
                    for i in range(x // domain_bit_count):
                        slice_count += 1

                    if (x // domain_bit_count) * domain_bit_count != x:
                        slice_count += 1
                else:
                    slice_item = [x]

                    while len(queue) > 0 and sum([y for y in slice_item]) + queue[0] <= domain_bit_count:
                        slice_item.append(queue.pop(0))

                    slice_count += 1

            return slice_count

        def get_slice_count(domain_bit_count: int) -> int:
            if restrictive_formula_params.transform_method == EampTransformMethod.SORTED_ROLLING_WINDOW:
                return get_slice_count_sorted_rolling_window(domain_bit_count)
            else:
                raise RuntimeError(f"Not implemented transform method {restrictive_formula_params.transform_method}")

        def generate_coefficients(j: int) -> Tuple[Tuple[int, ...], int, int]:
            pj = get_p(j + 1)[j]

            return (
                tuple([
                    random.get_random_int(0, pj - 1) for _ in range(
                        get_slice_count(get_variable_domain_size_max_bits(j))
                    )
                ]),
                random.get_random_int(0, pj - 1),
                random.get_random_int(0, pj - 1),
            )

        return EampInstanceParams(
            params=restrictive_formula_params,
            coefficients=tuple([
                tuple([
                    generate_coefficients(j) for _ in range(restrictive_formula_params.c[j])
                ]) for j in range(len(restrictive_formula_params.c))
            ]),
        )


def get_cn(max_model_count: int, G: float) -> int:
    """
    Returns the amount of entries in c required to allow a range that
    is greater than the maximum possible model count.
    """

    strictly_lower_cn = log2(log2(max_model_count / G)) + 1
    cn = int(floor(strictly_lower_cn)) + 1
    return min(max(cn, 1), get_highest_power_two_key_in_dict())


def get_p(cn: int) -> Tuple[int, ...]:
    """
    Returns the primes used for the partial hashes in the hash family
    that has at most cn entries in c.
    """

    return tuple([
        get_smallest_prime_above_or_equal_power_of_two(
            2 ** i
        ) for i in range(cn)
    ])


def get_pj(j: int) -> int:
    return get_p(j + 1)[j]


def get_range_size(c: Tuple[int, ...]) -> int:
    """
    Returns the size of the range of the hash family for
    the given c parameter.
    """

    p = get_p(len(c))
    return prod([p[i] ** c[i] for i in range(len(c))])


def get_variable_domain_size(j: int) -> int:
    """
    Returns the maximal number a variable in the
    j-th partial hash can have.
    """

    return get_p(j + 1)[j] - 1


def get_variable_domain_size_max_bits(j: int) -> int:
    """
    Returns the maximum amount of bits a variable in the j-th
    partial hash can have.
    """

    return int(floor(log2(get_variable_domain_size(j) + 1)))
