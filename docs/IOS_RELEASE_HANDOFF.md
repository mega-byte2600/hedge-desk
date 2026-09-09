# iOS MVP release handoff

## Verified in repository

- Objective-C UIKit target builds for the iOS Simulator.
- App icon and privacy manifest are packaged.
- Backend errors are visible instead of being presented as empty data.
- Release builds do not default to localhost.
- Backend is paper-only, Yellow-Sheet-gated, GET-only for Schwab, and has no
  order method or route.

## Account-owner actions required

1. In Schwab Developer Portal, create/approve the application and make its
   callback exactly match `SCHWAB_REDIRECT_URI`.
2. Store client ID and secret only in the backend environment; complete OAuth
   in a local browser. Never paste tokens into Git, Hermes, or App Store notes.
3. Deploy the backend behind authenticated HTTPS. Do not expose the current
   local development server directly to the internet.
4. In Xcode, select the owner's Apple Developer team, replace
   `com.hedgedesk.mvp` with the registered bundle identifier, and set the
   Release `HEDGE_DESK_API_BASE_URL` to that HTTPS deployment.
5. Supply App Store Connect support URL, privacy-policy URL, screenshots,
   category, age rating, financial-services disclosures, export-compliance
   answers, reviewer instructions, and test credentials if Apple requires them.
6. Archive and run Xcode validation. The account owner must inspect and
   explicitly authorize TestFlight/App Store upload and submission.

Publication does not authorize live trading. Any future order capability needs
a separately reviewed release architecture, deterministic Yellow Sheet/risk/
compliance/audit controls, and exact human authorization.
