"""Conventional exact-binomial inference; descriptive evidence, never authority."""

from dataclasses import dataclass
from decimal import Decimal, localcontext
from math import comb
from typing import Optional, Tuple


STAT_INFERENCE_VERSION = "exact-binomial-wilson-1.0.0"
_WILSON_95_Z = Decimal("1.959963984540054")


@dataclass(frozen=True)
class DirectionalInferencePolicy:
    null_hit_rate: Decimal = Decimal("0.5")
    alpha: Decimal = Decimal("0.005")
    confidence_level: Decimal = Decimal("0.95")
    minimum_sample_size: int = 100

    def __post_init__(self) -> None:
        values = (self.null_hit_rate, self.alpha, self.confidence_level)
        if any(not isinstance(value, Decimal) or not value.is_finite() for value in values):
            raise ValueError("inference probabilities must be finite Decimals")
        if not Decimal("0") < self.null_hit_rate < Decimal("1"):
            raise ValueError("null hit rate must be between zero and one")
        if not Decimal("0") < self.alpha < Decimal("1"):
            raise ValueError("significance alpha must be between zero and one")
        if self.confidence_level != Decimal("0.95"):
            raise ValueError("this validated Wilson implementation supports 95% only")
        if type(self.minimum_sample_size) is not int or self.minimum_sample_size <= 0:
            raise ValueError("minimum sample size must be a positive integer")


@dataclass(frozen=True)
class DirectionalInference:
    method_version: str
    sample_size: int
    successes: int
    observed_hit_rate: Decimal
    null_hit_rate: Decimal
    alpha: Decimal
    confidence_level: Decimal
    one_sided_exact_p_value: Optional[Decimal]
    wilson_confidence_interval: Optional[Tuple[Decimal, Decimal]]
    statistically_significant: Optional[bool]
    inference_status: str
    trade_authorized: bool = False


def _exact_upper_binomial_tail(successes: int, sample_size: int, p: Decimal) -> Decimal:
    with localcontext() as context:
        context.prec = 50
        q = Decimal("1") - p
        return sum(
            (
                Decimal(comb(sample_size, k))
                * (p ** k)
                * (q ** (sample_size - k))
                for k in range(successes, sample_size + 1)
            ),
            Decimal("0"),
        )


def _wilson_95(successes: int, sample_size: int) -> Tuple[Decimal, Decimal]:
    with localcontext() as context:
        context.prec = 50
        n = Decimal(sample_size)
        rate = Decimal(successes) / n
        z2 = _WILSON_95_Z ** 2
        denominator = Decimal("1") + z2 / n
        center = (rate + z2 / (Decimal("2") * n)) / denominator
        margin = (
            _WILSON_95_Z
            * ((rate * (Decimal("1") - rate) / n + z2 / (Decimal("4") * n * n)).sqrt())
            / denominator
        )
        return max(Decimal("0"), center - margin), min(Decimal("1"), center + margin)


def evaluate_directional_hits(
    outcomes: Tuple[bool, ...],
    policy: DirectionalInferencePolicy = DirectionalInferencePolicy(),
) -> DirectionalInference:
    if not outcomes:
        raise ValueError("directional inference requires outcomes")
    if any(type(value) is not bool for value in outcomes):
        raise ValueError("directional outcomes must be booleans")
    successes = sum(outcomes)
    sample_size = len(outcomes)
    hit_rate = Decimal(successes) / Decimal(sample_size)
    if sample_size < policy.minimum_sample_size:
        return DirectionalInference(
            STAT_INFERENCE_VERSION,
            sample_size,
            successes,
            hit_rate,
            policy.null_hit_rate,
            policy.alpha,
            policy.confidence_level,
            None,
            None,
            None,
            "INSUFFICIENT_SAMPLE",
        )
    p_value = _exact_upper_binomial_tail(
        successes, sample_size, policy.null_hit_rate
    )
    return DirectionalInference(
        STAT_INFERENCE_VERSION,
        sample_size,
        successes,
        hit_rate,
        policy.null_hit_rate,
        policy.alpha,
        policy.confidence_level,
        p_value,
        _wilson_95(successes, sample_size),
        p_value <= policy.alpha,
        "VALIDATED_METHOD_RESULT",
    )
