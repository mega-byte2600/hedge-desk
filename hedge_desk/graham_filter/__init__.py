"""Graham Filter — deterministic candidate assessment (paper research only)."""
from .engine import (
    Assessment,
    Candidate,
    Standards,
    PROTOTYPE_STANDARDS,
    assess,
    assess_all,
    market_regime,
)
from .adapter import adapt, adapt_assess
from .contract import (
    DEFAULT_FILTER,
    FILTER_MODES,
    VERDICTS,
    apply_filter,
    to_batch,
    to_dict,
)

__all__ = [
    "Assessment", "Candidate", "Standards", "PROTOTYPE_STANDARDS",
    "assess", "assess_all", "market_regime",
    "adapt", "adapt_assess",
    "DEFAULT_FILTER", "FILTER_MODES", "VERDICTS",
    "apply_filter", "to_batch", "to_dict",
]
