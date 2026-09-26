import Foundation

// MARK: - Learn snapshot: real desk data for the Learn tab
//
// Generated from the nightly research report by scripts/export_learn_snapshot.py.
// Every figure carries its as-of date and source. Screened contracts are research
// output only (trade_authorized=false everywhere in the pipeline) — this file
// adds no recommendation and performs no financial calculation.

struct LearnSnapshot: Decodable {
    let schemaVersion: String
    let generatedAt: String?
    let asOf: String
    let isCurrent: Bool
    let vix: MarketLevel
    let wti: MarketLevel
    let spyChain: ChainStatus
    let rates: RatesStatus
    let cspScreen: [ScreenedContract]
    let candidateCount: Int?
    let eodStatus: String

    struct MarketLevel: Decodable {
        let level: Double?
        let asOf: String
        let source: String
        let mode: String
    }
    struct ChainStatus: Decodable {
        let mode: String
        let structures: Int
        let asOf: String
        let source: String
    }
    struct RatesStatus: Decodable {
        let mode: String
        let note: String
    }
    struct ScreenedContract: Decodable, Identifiable {
        var id: String { symbol + (expiration ?? "") + (strike ?? "") }
        let symbol: String
        let strike: String?
        let expiration: String?
        let dte: Int?
        let creditPerShare: String?
        let collateral: String?
        let returnOnCollateral: Double?
        let fitsRules: Bool
        let screenOutReason: String?
        let source: String

        enum CodingKeys: String, CodingKey {
            case symbol, strike, expiration, dte, source
            case creditPerShare = "credit_per_share"
            case collateral
            case returnOnCollateral = "return_on_collateral"
            case fitsRules = "fits_rules"
            case screenOutReason = "screen_out_reason"
        }
    }

    enum CodingKeys: String, CodingKey {
        case asOf = "as_of"
        case isCurrent = "is_current"
        case vix, wti, rates
        case schemaVersion = "schema_version"
        case generatedAt = "generated_at"
        case spyChain = "spy_chain"
        case cspScreen = "csp_screen"
        case candidateCount = "candidate_count"
        case eodStatus = "eod_status"
    }

    /// Bundled snapshot, or nil when the resource is missing or undecodable.
    /// Callers must show an honest fallback — never a fabricated number.
    static func load() -> LearnSnapshot? {
        guard let url = Bundle.main.url(forResource: "LearnSnapshot", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let snap = try? JSONDecoder().decode(LearnSnapshot.self, from: data),
              snap.schemaVersion.hasPrefix("hedge-desk-learn-snapshot-") else { return nil }
        return snap
    }
}

/// "2026-09-25" -> "Sep 25, 2026". Manual mapping avoids locale surprises.
func prettyDate(_ iso: String) -> String {
    let parts = iso.split(separator: "-")
    guard parts.count == 3, let month = Int(parts[1]), (1...12).contains(month) else { return iso }
    let names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return "\(names[month - 1]) \(Int(parts[2]) ?? 0), \(parts[0])"
}
