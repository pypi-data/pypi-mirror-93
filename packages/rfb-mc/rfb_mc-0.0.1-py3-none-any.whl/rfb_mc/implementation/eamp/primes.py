from typing import Dict, Tuple
from functools import lru_cache
import os

primes_power_two_file_name = os.path.join(os.path.dirname(__file__), "primes_power_two.txt")


@lru_cache(1)
def read_primes_power_two_dict() -> Dict[int, int]:
    def parse_line(line: str) -> Tuple[int, int]:
        ns, ps = line.split(" ")
        return int(ns, 10), int(ps, 10)

    with open(primes_power_two_file_name, "r") as f:
        lines = f.readlines()

    return {
        n: p for n, p in map(parse_line, lines)
    }


def get_smallest_prime_above_or_equal_power_of_two(n: int) -> int:
    """
    Returns the smallest prime that is >= 2 ** n
    """

    n = max(n, 0)

    power_two_dict = read_primes_power_two_dict()

    if n in power_two_dict:
        return power_two_dict[n]
    else:
        raise ValueError(f"No smallest prime for power n={n} was specified")


def get_highest_power_two_key_in_dict() -> int:
    power_two_dict = read_primes_power_two_dict()
    return max(power_two_dict.keys())
