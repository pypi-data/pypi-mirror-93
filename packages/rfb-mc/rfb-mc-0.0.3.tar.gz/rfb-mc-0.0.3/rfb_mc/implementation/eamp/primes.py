from rfb_mc.implementation.eamp.primes_power_two import primes_power_two_dict


def get_smallest_prime_above_or_equal_power_of_two(n: int) -> int:
    """
    Returns the smallest prime that is >= 2 ** n
    """

    n = max(n, 0)

    if n in primes_power_two_dict:
        return primes_power_two_dict[n]
    else:
        raise ValueError(f"No smallest prime for power n={n} was specified")


def get_highest_power_two_key_in_dict() -> int:
    return max(primes_power_two_dict.keys())
