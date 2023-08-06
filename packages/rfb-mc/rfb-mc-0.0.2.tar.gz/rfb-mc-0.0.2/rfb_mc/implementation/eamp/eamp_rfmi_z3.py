import z3
from math import log2, ceil
from typing import Type, List, Tuple
from rfb_mc.implementation.eamp.eamp_rfm import EampInstanceParams, EampRfm, EampTransformMethod, \
    get_variable_domain_size_max_bits, get_pj
from rfb_mc.implementation.runner_z3 import RfmiGenerationArgsZ3
from rfb_mc.restrictive_formula_module_implementation import RestrictiveFormulaModuleImplementationBase
from rfb_mc.types import Params


class EampRfmiZ3(RestrictiveFormulaModuleImplementationBase[EampInstanceParams, RfmiGenerationArgsZ3, z3.BoolRef]):
    @classmethod
    def get_restrictive_formula_module(
        cls,
    ) -> Type[EampRfm]:
        return EampRfm

    @classmethod
    def generate_restrictive_formula(
        cls,
        params: Params,
        instance_params: EampInstanceParams,
        args: RfmiGenerationArgsZ3,
    ) -> z3.BoolRef:
        def get_slices_sorted_rolling_window(domain_bit_count: int) -> List[z3.BitVecRef]:
            slices = []

            queue = sorted(args.variables, key=lambda x: x.size())

            while len(queue) > 0:
                x = queue.pop(0)

                if x.size() >= domain_bit_count:
                    for i in range(x.size() // domain_bit_count):
                        slices.append(
                            z3.Extract(i * domain_bit_count + domain_bit_count - 1, i * domain_bit_count, x)
                        )

                    if (x.size() // domain_bit_count) * domain_bit_count != x.size():
                        rem_slice_size = x.size() % domain_bit_count
                        slices.append(
                            z3.ZeroExt(
                                domain_bit_count - rem_slice_size,
                                z3.Extract(x.size() - 1, x.size() - rem_slice_size, x)
                            )
                        )
                else:
                    slice_item = [x]

                    while len(queue) > 0 and sum([y.size() for y in slice_item]) + queue[0].size() <= domain_bit_count:
                        slice_item.append(queue.pop(0))

                    slices.append(z3.Concat(slice_item) if len(slice_item) > 1 else slice_item[0])

            return slices

        def get_slices(domain_bit_count: int) -> List[z3.BitVecRef]:
            if instance_params.params.transform_method == EampTransformMethod.SORTED_ROLLING_WINDOW:
                return get_slices_sorted_rolling_window(domain_bit_count)
            else:
                raise RuntimeError(f"Not implemented transform method {instance_params.params.transform_method}")

        def make_hash_equation(j: int, var_b: Tuple[int], b1: int, b2: int):
            pj = get_pj(j)
            domain_bit_count = get_variable_domain_size_max_bits(j)
            bc = max(int(ceil(log2(pj + 1))), get_variable_domain_size_max_bits(j))
            slices = get_slices(domain_bit_count)

            return z3.URem(
                z3.Sum([
                    z3.ZeroExt(bc - s.size(), s) * z3.BitVecVal(var_b[i], bc) for i, s in enumerate(slices)
                ]) + z3.BitVecVal(b1, bc),
                z3.BitVecVal(pj, bc)
            ) == z3.BitVecVal(b2, bc)

        return z3.And([
            make_hash_equation(j, var_b, b1, b2)
            for j in range(len(instance_params.coefficients))
            for var_b, b1, b2 in instance_params.coefficients[j]
        ])
