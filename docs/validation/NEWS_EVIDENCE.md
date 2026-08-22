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
