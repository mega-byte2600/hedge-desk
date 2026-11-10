# Retired: membership and sign-in

The sign-in, membership, subscription, investor-seat, and broker-link surfaces have
been removed from the public Hedge Desk console. Their legacy API routes return
`410 Gone`. Do not configure SMTP, membership, Supabase Auth, GP invite, or Schwab
broker-link settings for this service.

Historical membership implementation and database records are retained in the
repository for recovery and audit; the web service no longer imports or exposes
that functionality. This retirement does not affect public market-data feeds,
company filings, research reports, or paper-only risk and compliance controls.
