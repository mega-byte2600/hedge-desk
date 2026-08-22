"""Account eligibility gate with explicit, auditable rejection reasons."""

from typing import List

from hedge_desk.domain import Account, AccountType, ProductType, TradeCandidate


def account_gate(account: Account, candidate: TradeCandidate) -> List[str]:
    """Return blocking reason codes; an empty result means eligible for paper."""
    reasons: List[str] = []
    product = candidate.product_type

    if product is ProductType.UNDEFINED_RISK_OPTION:
        reasons.append("UNDEFINED_RISK_OPTION_PROHIBITED")

    if product in {
        ProductType.DEFINED_RISK_OPTION,
        ProductType.UNDEFINED_RISK_OPTION,
    }:
        if not account.options_approved:
            reasons.append("OPTIONS_APPROVAL_REQUIRED")
        if (
            not account.options_disclosure_version
            or account.options_disclosure_acknowledged_at is None
        ):
            reasons.append("OPTIONS_DISCLOSURE_ACKNOWLEDGEMENT_REQUIRED")
        elif account.options_disclosure_acknowledged_at > candidate.quote_timestamp:
            reasons.append("OPTIONS_DISCLOSURE_ACKNOWLEDGED_AFTER_CANDIDATE")
        if not account.broker_options_policy_version:
            reasons.append("BROKER_OPTIONS_POLICY_REQUIRED")

    if product is ProductType.FUTURE:
        if not account.futures_approved:
            reasons.append("FUTURES_APPROVAL_REQUIRED")
        if account.account_type in {
            AccountType.TRADITIONAL_IRA,
            AccountType.ROTH_IRA,
        }:
            reasons.append("FUTURES_BLOCKED_IN_IRA_MVP")

    notional = candidate.entry_price * candidate.quantity
    if product is ProductType.EQUITY and notional > account.cash:
        reasons.append("INSUFFICIENT_CASH")

    return sorted(set(reasons))
