"""Demonstrate the deterministic paper-only decision workflow."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal

from hedge_desk.core.decision import evaluate_candidate
from hedge_desk.domain import Account, AccountType, ProductType, TradeCandidate


def main() -> None:
    evaluated_at = datetime(2026, 7, 28, 13, 0, tzinfo=timezone.utc)
    account = Account(
        account_id="paper-individual-001",
        account_type=AccountType.INDIVIDUAL,
        equity=Decimal("100000"),
        cash=Decimal("50000"),
        options_approved=True,
    )
    candidate = TradeCandidate(
        candidate_id="demo-aapl-001",
        symbol="AAPL",
        product_type=ProductType.EQUITY,
        quantity=10,
        entry_price=Decimal("200"),
        max_loss=Decimal("500"),
        expected_win=Decimal("1000"),
        win_probability=Decimal("0.55"),
        quote_timestamp=evaluated_at - timedelta(minutes=1),
        average_daily_dollar_volume=Decimal("1000000000"),
        thesis="Demonstration candidate with bounded loss and positive expectancy.",
        invalidation="Block if the documented valuation premise fails.",
    )
    decision = evaluate_candidate(account, candidate, evaluated_at)
    print(decision)


if __name__ == "__main__":
    main()

