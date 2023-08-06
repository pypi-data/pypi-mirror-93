from fractions import Fraction
from math import ceil, comb


def majority_vote_error_probability_native(
    alpha: Fraction, r: int,
) -> Fraction:
    return sum([
        comb(r, rj) * (alpha ** r) * ((1 - alpha) ** (r - rj))
        for rj in range(ceil(r / 2), r + 1)
    ])


def majority_vote_error_probability(
    alpha: Fraction, positive_votes: int, negative_votes: int,
) -> Fraction:
    """
    Returns bound on error probability of majority vote outcome.
    :param alpha: Error probability of procedure
    :param positive_votes:
    :param negative_votes:
    """

    # amount of votes that could have been added to the loosing side that would still have lost
    margin = abs(positive_votes - negative_votes)

    # amount of votes the majority vote has effectively had, considering how many could have been added without
    # possibility of changing the outcome
    r = positive_votes + negative_votes + margin

    return majority_vote_error_probability_native(alpha, r)


def multi_majority_vote_iteration_count_to_ensure_beta(
    alpha: Fraction, beta: Fraction, max_majority_voting_countings: int,
) -> int:
    """
    Returns an amount of iterations for each majority vote counting such that
    the error probability of any of the majority vote counting to fail is below beta.
    :param alpha: Error probability of the procedures in the majority vote counting
    :param beta: Desired upper bound on error probability of any majority vote counting failing
    :param max_majority_voting_countings: Maximum amount of expected majority vote counting procedures
    """

    r = 1
    while max_majority_voting_countings * majority_vote_error_probability_native(alpha, r) > beta:
        r += 1

    return r
