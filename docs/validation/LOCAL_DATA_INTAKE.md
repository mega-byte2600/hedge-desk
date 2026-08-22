# Local data intake

Use the local intake command for permission-cleared or licensed payloads that
must stay outside the public repository. The command reads and hashes the file;
it does not copy or commit it.

Create a sibling JSON envelope with exactly these fields:

```json
{
  "schema_version": "hedge-desk-observation-1.0.0",
  "artifact_id": "unique-snapshot-id",
  "payload_kind": "option_chain",
  "source_id": "your-source-account",
  "license_id": "your-entitlement-id",
  "source_as_of": "2026-08-22T08:00:00-07:00",
  "received_at": "2026-08-22T08:00:01-07:00",
  "payload_sha256": "sha256-of-the-exact-local-file",
  "synthetic": false,
  "redistribution_allowed": false
}
```

Validate it locally:

Create a separate point-in-time exchange-session evidence file using schema
`hedge-desk-market-session-1.0.0`:

```json
{
  "schema_version": "hedge-desk-market-session-1.0.0",
  "venue": "OPRA",
  "regular_open": "2026-08-22T06:30:00-07:00",
  "regular_close": "2026-08-22T13:00:00-07:00",
  "received_at": "2026-08-22T05:00:00-07:00",
  "calendar_artifact_sha256": "sha256-of-the-exact-calendar-artifact"
}
```

Then validate and scan:

```bash
python3 -m hedge_desk.cli \
  --validate-data-envelope snapshot.envelope.json \
  --payload /private/path/snapshot.json \
  --validate-option-snapshot \
  --scan-vertical-spreads \
  --market-session-evidence /private/path/market-session.json \
  --minimum-seconds-before-close 900 \
  --decision-cutoff 2026-08-22T08:00:02-07:00 \
  --max-age-seconds 120
```

Exit code `0` means the artifact passed the declared provenance,
point-in-time, hash, and freshness gate. Exit code `2` means it was blocked.
Admissibility does not grant redistribution rights and does not validate the
financial meaning of vendor fields.

With `--validate-option-snapshot`, the payload must use schema version
`hedge-desk-option-snapshot-1.0.0`. Money fields must be decimal strings, quote
times must include offsets, option and underlying symbols/sources must agree,
contracts must be unique, and unknown fields are rejected. The command outputs
only structural metadata and contract IDs—not the licensed quote payload.

`--scan-vertical-spreads` enumerates all executable-side defined-risk vertical
pairs under the checked-in liquidity and timing policy. It does not select a
best trade, estimate probability, calculate Risk of Ruin, or authorize a trade.
The CLI withholds all candidate handoffs when market-session evidence is absent
or blocked. An admitted handoff binds the calendar hash, decision time, and
latest entry time; it still stops at `VALIDATED_RISK_INPUT_REQUIRED`.
