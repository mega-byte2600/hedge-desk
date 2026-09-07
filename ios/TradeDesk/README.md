# Native Trade Desk for iPhone

Native SwiftUI app for iOS 16 or later. No npm, CocoaPods, Swift package,
subscription, brokerage adapter, or local backend is required.

## Fastest free installation on your own iPhone

1. On your Mac, open `TradeDesk.xcodeproj` in Xcode 15 or later.
2. In Xcode Settings > Accounts, sign in with your Apple Account.
3. Select the TradeDesk target > Signing & Capabilities. Choose your Personal
   Team and leave Automatically manage signing enabled. If the bundle ID is
   unavailable, change it to a unique identifier under your own name.
4. Connect and trust your iPhone. Enable Developer Mode when Xcode requests it.
5. Choose the iPhone as the run destination and press Run (Command-R).

A free Personal Team is for personal device testing, with provisioning limits
and periodic reinstallation. A TestFlight download requires Apple Developer
Program membership, an App Store Connect record, a signed archive, and Apple's
applicable processing/review. No signing credentials belong in this repository.

Apple guidance:
https://developer.apple.com/support/compare-memberships/
https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases

## Behavior

- Native desk navigation and immutable engine gate/metric displays.
- Native scenario search, blocked-case filtering, and evidence inspection.
- Yellow Sheets saved atomically in the app's Application Support directory.
- Native share sheet for reports and notes; notes never upload to the website.
- Bundled synthetic report opens offline. Pull to refresh fetches the existing
  public HTTPS report snapshot. Refresh does not run the Python engine.
- Snapshot provenance, synthetic labels, and the reference model's unvalidated
  RoR status remain visible. The app performs no financial calculations.
- An invalid/failed refresh preserves the last displayed report and shows an
  error. The app checks the report envelope/paper boundary for display; the
  existing Python publication validator remains upstream and authoritative.
- Web-browser notes and iPhone notes are separate. Deleting the app may delete
  its notes; export a backup first.

## macOS verification

```sh
xcodebuild -project TradeDesk.xcodeproj -scheme TradeDesk \
  -sdk iphonesimulator -configuration Debug CODE_SIGNING_ALLOWED=NO build
```

Then run on a simulator/device and inspect all four tabs, refresh/error states,
scenario filtering, note persistence after relaunch, and native sharing.

This source was prepared in Linux, where Xcode and Apple iOS SDKs are absent.
It has not been compiled, signed, or device-tested here. No installable IPA or
TestFlight release is claimed. The older `../HedgeDeskObjC` prototype is retained
for reference and is not part of this target.
