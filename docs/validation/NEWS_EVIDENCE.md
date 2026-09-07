# News and RSS evidence boundary

RSS, newsgroups, news APIs, filings, and agency feeds can reduce event-data
gaps, but delivery method is not a license and a headline is not a trade.

`evaluate_news_batch` admits only public, licensed/permission-identified,
HTTPS-sourced, content-hashed, timezone-aware, point-in-time observations inside
the declared freshness window. Duplicate URL/content, private information,
look-ahead, missing licenses, bad hashes, and stale evidence fail closed.

The output is research evidence only. It cannot authorize a trade and never
allows raw content into the public repository. Reuters or another commercial
publisher requires a purchased entitlement whose terms cover the intended API,
automation, storage, model use, and derived outputs; an RSS endpoint alone does
not grant those rights. Commit metadata, hashes, schemas, and permitted derived
facts—not copyrighted vendor payloads.

## Papers With Backtest: All Daily News

The `hedge_desk.data.pwb_news` adapter loads the vendor dataset by its canonical
identifier, `All-Daily-News`, using `pwb-toolbox`. The client accepts either
`PWB_API_KEY` or `HF_ACCESS_TOKEN`; `PWB_NEWS_LICENSE_ID` should identify the
operator's reviewed entitlement without containing a secret or account number.

The adapter recognizes the published dataset fields for symbols, datetime,
title, URL, authors, summary, source, topics, overall sentiment, and
symbol-specific sentiment. Vendor headlines, summaries, authors, topics, and
URLs remain in memory and are not returned in the derived result. The durable
result contains only symbol, article count, average symbol sentiment, latest
publication time, and evidence hashes.

The source page does not document a timezone guarantee and its example uses a
midnight timestamp. Therefore naive datetimes require an explicitly reviewed
source timezone, and derived observations receive a conservative one-day
publication embargo by default. This prevents same-day backtests from silently
using news that may not have been available at the simulated decision time.
Changing the embargo requires separate timestamp-semantics validation.

Installation and a minimal research-only run:

```bash
python -m pip install -e '.[news]'
export PWB_API_KEY='stored-outside-the-repository'
```

```python
from datetime import datetime, timezone
from hedge_desk.data import evaluate_pwb_daily_news, load_pwb_daily_news

frame = load_pwb_daily_news()
result = evaluate_pwb_daily_news(
    frame,
    license_id="reviewed-pwb-entitlement",
    evaluated_at=datetime.now(timezone.utc),
    source_timezone=timezone.utc,
)
```

The source timezone in this example is illustrative, not a vendor assertion.
The result stays research-only and cannot clear deterministic risk, compliance,
human authorization, or Back Office controls.
