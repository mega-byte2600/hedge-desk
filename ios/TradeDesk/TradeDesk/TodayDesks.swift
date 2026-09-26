import Foundation
import SwiftUI

// MARK: - Today tab: last night's real desk output, paper only.
//
// Fetches three live research feeds from the user's own hedge-desk server
// (paper-only: no orders, no trade authorization):
//   GET /api/earnings-candidates  — real SEC EDGAR EPS actuals
//   GET /api/macro-candidates     — real FRED macro / rates observations
//   GET /api/nightly-outcomes     — observed paper outcomes + yellow sheets
//
// Every number is shown with its source. Loading, empty, and error states
// are explicit; nothing is ever fabricated. If a feed is missing or the
// server is unreachable, the tab says so plainly.

private let defaultApiBaseURL = "http://localhost:8765"

// MARK: - Feed models (snake_case JSON -> camelCase via the decoder)

/// A number that may arrive as a JSON number or as a placeholder string ("?").
private struct LenientDouble: Decodable {
    let value: Double?
    init(from decoder: Decoder) throws {
        let box = try decoder.singleValueContainer()
        if let d = try? box.decode(Double.self) { value = d; return }
        if let s = try? box.decode(String.self) { value = Double(s); return }
        value = nil
    }
}

struct EpsObservation: Decodable {
    let latestQuarterlyEps: Double?
    let latestQuarterlyPeriod: String?
    let priorQuarterlyEps: Double?
    let priorQuarterlyPeriod: String?
    let latestFyEps: Double?
    let latestFyPeriod: String?

    private enum Keys: String, CodingKey {
        case latestQuarterlyEps, latestQuarterlyPeriod, priorQuarterlyEps,
             priorQuarterlyPeriod, latestFyEps, latestFyPeriod
    }
    private static func number(_ c: KeyedDecodingContainer<Keys>, _ k: Keys) -> Double? {
        (try? c.decodeIfPresent(LenientDouble.self, forKey: k))??.value
    }
    private static func period(_ c: KeyedDecodingContainer<Keys>, _ k: Keys) -> String? {
        guard let raw = try? c.decodeIfPresent(String.self, forKey: k),
              !raw.isEmpty, raw != "?" else { return nil }
        return raw
    }
    init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: Keys.self)
        latestQuarterlyEps = Self.number(c, .latestQuarterlyEps)
        latestQuarterlyPeriod = Self.period(c, .latestQuarterlyPeriod)
        priorQuarterlyEps = Self.number(c, .priorQuarterlyEps)
        priorQuarterlyPeriod = Self.period(c, .priorQuarterlyPeriod)
        latestFyEps = Self.number(c, .latestFyEps)
        latestFyPeriod = Self.period(c, .latestFyPeriod)
    }
}

struct EarningsCandidate: Decodable, Identifiable {
    var id: String { cik + ":" + symbol }
    let deskId: String
    let symbol: String
    let cik: String
    let instrumentType: String
    let stage: String
    let method: String
    let observation: EpsObservation?
    let evidenceNeeded: String?
    let dataSource: String?
    let tradeAuthorized: Bool
}

struct EarningsFeed: Decodable {
    let schemaVersion: String?
    let mode: String?
    let candidateDefinition: String?
    let reportSha256: String?
    let candidates: [EarningsCandidate]
    let reason: String?
}

struct MacroCandidate: Decodable, Identifiable {
    var id: String { symbol }
    let deskId: String
    let symbol: String
    let instrumentType: String
    let stage: String
    let method: String
    let evidenceNeeded: String?
    let dataSource: String?
    let tradeAuthorized: Bool
}

struct MacroFeed: Decodable {
    let schemaVersion: String?
    let mode: String?
    let candidateDefinition: String?
    let reportSha256: String?
    let candidates: [MacroCandidate]
    let reason: String?
}

struct OutcomeSummary: Decodable {
    let mode: String?
    let entryCount: Int?
    let symbolCount: Int?
    let outcomeCounts: [String: Int]?
    let note: String?
}

struct YellowSheetSummary: Decodable {
    let mode: String?
    let sheetCount: Int?
    let symbolCount: Int?
    let byDecision: [String: Int]?
    let note: String?
}

struct NightlyOutcomes: Decodable {
    let schemaVersion: String?
    let mode: String?
    let reportSha256: String?
    let paperOutcomeSummary: OutcomeSummary?
    let yellowSheets: YellowSheetSummary?
    let tradeAuthorized: Bool?
    let note: String?
    let status: String?
    let reason: String?
    var unavailable: Bool { status == "NIGHTLY_REPORT_UNAVAILABLE" }
}

// MARK: - Store

enum FeedState<T> {
    case idle, loading, loaded(T), failed(String)
}

@MainActor
final class TodayStore: ObservableObject {
    // Persisted server address. @Published (not @AppStorage) so views can
    // bind with $store.apiBaseURL; the value is mirrored to UserDefaults.
    @Published var apiBaseURL: String = UserDefaults.standard.string(forKey: "todayApiBaseURL") ?? defaultApiBaseURL {
        didSet { UserDefaults.standard.set(apiBaseURL, forKey: "todayApiBaseURL") }
    }
    @Published var earnings: FeedState<EarningsFeed> = .idle
    @Published var macro: FeedState<MacroFeed> = .idle
    @Published var outcomes: FeedState<NightlyOutcomes> = .idle
    @Published var loading = false

    func refresh() async {
        guard !loading else { return }
        loading = true
        defer { loading = false }
        earnings = .loading
        macro = .loading
        outcomes = .loading
        async let e: FeedState<EarningsFeed> = fetch(path: "/api/earnings-candidates")
        async let m: FeedState<MacroFeed> = fetch(path: "/api/macro-candidates")
        async let o: FeedState<NightlyOutcomes> = fetch(path: "/api/nightly-outcomes")
        earnings = await e
        macro = await m
        outcomes = await o
    }

    private func fetch<T: Decodable>(path: String) async -> FeedState<T> {
        let base = apiBaseURL.trimmingCharacters(in: .whitespacesAndNewlines)
            .trimmingCharacters(in: CharacterSet(charactersIn: "/"))
        guard !base.isEmpty, let url = URL(string: base + path), url.host != nil else {
            return .failed("The server address looks wrong. Tap the gear icon and check it.")
        }
        do {
            var request = URLRequest(url: url)
            request.timeoutInterval = 20
            request.cachePolicy = .reloadIgnoringLocalCacheData
            let (data, response) = try await URLSession.shared.data(for: request)
            guard let http = response as? HTTPURLResponse else {
                return .failed("The server did not answer.")
            }
            guard (200...299).contains(http.statusCode) else {
                // /api/nightly-outcomes answers 503 with a JSON body explaining why.
                if let message = Self.serverMessage(from: data) { return .failed(message) }
                return .failed("The server returned status \(http.statusCode). Is the nightly batch running?")
            }
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            do {
                return .loaded(try decoder.decode(T.self, from: data))
            } catch {
                return .failed("The server answered, but the data was not in the expected shape.")
            }
        } catch {
            return .failed("Could not reach the server at \(base). Start the hedge-desk server (port 8765), or fix the address under the gear icon.")
        }
    }

    private static func serverMessage(from data: Data) -> String? {
        guard let obj = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return nil }
        if let reason = obj["reason"] as? String, !reason.isEmpty { return reason }
        if let status = obj["status"] as? String, !status.isEmpty { return "Server status: \(status)" }
        return nil
    }
}

// MARK: - Views

private struct SourceCaption: View {
    let text: String
    var body: some View {
        Text("source: \(text)").font(.caption2).foregroundStyle(.secondary).italic()
    }
}

private struct FeedError: View {
    let message: String
    var body: some View {
        Label(message, systemImage: "wifi.exclamationmark")
            .font(.footnote).foregroundStyle(.red)
    }
}

struct TodayView: View {
    @StateObject private var store = TodayStore()
    @State private var showSettings = false

    var body: some View {
        NavigationStack {
            List {
                Section {
                    VStack(alignment: .leading, spacing: 6) {
                        Label("TODAY'S RESEARCH", systemImage: "sun.max").font(.caption.weight(.bold))
                        Text("Last night's batch, straight from your server. Research only — this app places no orders.")
                            .font(.footnote).foregroundStyle(.secondary)
                    }.padding(.vertical, 4)
                }
                earningsSection
                macroSection
                outcomesSection
                Section {
                    Text("Everything here is research input, not a trade signal. Every number shows its source so you can trace it back.")
                        .font(.footnote).foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Today")
            .task { await store.refresh() }
            .refreshable { await store.refresh() }
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button { showSettings = true } label: { Image(systemName: "gear") }
                        .accessibilityLabel("Server settings")
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button { Task { await store.refresh() } } label: {
                        if store.loading { ProgressView() } else { Image(systemName: "arrow.clockwise") }
                    }.disabled(store.loading).accessibilityLabel("Reload today's research")
                }
            }
            .sheet(isPresented: $showSettings) { ApiSettingsView(store: store) }
        }
    }

    // MARK: Earnings

    @ViewBuilder
    private var earningsSection: some View {
        Section("Earnings desk") {
            switch store.earnings {
            case .idle, .loading:
                HStack { Spacer(); ProgressView("Loading earnings…"); Spacer() }
            case .failed(let message):
                FeedError(message: message)
            case .loaded(let feed):
                if feed.candidates.isEmpty {
                    Text(feed.reason ?? "No earnings observations in the latest batch.")
                        .font(.footnote).foregroundStyle(.secondary)
                } else {
                    ForEach(feed.candidates) { candidate in
                        EarningsRow(candidate: candidate)
                    }
                }
            }
        }
    }

    // MARK: Macro

    @ViewBuilder
    private var macroSection: some View {
        Section("Macro backdrop") {
            switch store.macro {
            case .idle, .loading:
                HStack { Spacer(); ProgressView("Loading macro…"); Spacer() }
            case .failed(let message):
                FeedError(message: message)
            case .loaded(let feed):
                if feed.candidates.isEmpty {
                    Text(feed.reason ?? "Macro data is currently withheld. Showing nothing is safer than showing a wrong number.")
                        .font(.footnote).foregroundStyle(.secondary)
                } else {
                    ForEach(feed.candidates) { candidate in
                        MacroRow(candidate: candidate)
                    }
                }
            }
        }
    }

    // MARK: Outcomes

    @ViewBuilder
    private var outcomesSection: some View {
        Section("Paper outcomes") {
            switch store.outcomes {
            case .idle, .loading:
                HStack { Spacer(); ProgressView("Loading outcomes…"); Spacer() }
            case .failed(let message):
                FeedError(message: message)
            case .loaded(let payload):
                if payload.unavailable {
                    Text(payload.reason ?? "The nightly report is not available.")
                        .font(.footnote).foregroundStyle(.secondary)
                } else {
                    OutcomesBody(payload: payload)
                }
            }
        }
    }
}

private struct EarningsRow: View {
    let candidate: EarningsCandidate

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(candidate.symbol).font(.headline)
            Text("Reported earnings per share — actuals from company filings, not estimates.")
                .font(.caption).foregroundStyle(.secondary)
            if let obs = candidate.observation {
                EpsLine(label: "Latest quarter", eps: obs.latestQuarterlyEps, period: obs.latestQuarterlyPeriod)
                EpsLine(label: "Prior quarter", eps: obs.priorQuarterlyEps, period: obs.priorQuarterlyPeriod)
                EpsLine(label: "Latest fiscal year", eps: obs.latestFyEps, period: obs.latestFyPeriod)
            } else {
                Text("EPS detail not available for this entry.").font(.caption).foregroundStyle(.secondary)
            }
            SourceCaption(text: "SEC EDGAR companyfacts · nightly batch")
            Text("Research input only — not a trade signal.")
                .font(.caption2).foregroundStyle(.secondary)
        }.padding(.vertical, 4)
    }
}

private struct EpsLine: View {
    let label: String
    let eps: Double?
    let period: String?

    var body: some View {
        HStack {
            Text(label).font(.subheadline).foregroundStyle(.secondary)
            Spacer()
            if let eps {
                Text(String(format: "$%.2f", eps)).font(.subheadline.monospaced())
                if let period {
                    Text("· ended \(period)").font(.caption).foregroundStyle(.secondary)
                }
            } else {
                Text("not reported").font(.caption).foregroundStyle(.secondary)
            }
        }
    }
}

private let macroLabels: [String: String] = [
    "UNRATE": "Unemployment rate",
    "DGS5": "5-year Treasury yield",
    "DGS30": "30-year Treasury yield",
    "FEDFUNDS": "Fed funds rate",
    "DGS10": "10-year Treasury yield",
]

private struct MacroRow: View {
    let candidate: MacroCandidate

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(macroLabels[candidate.symbol] ?? candidate.symbol).font(.headline)
            // The server's method line already reads as plain language,
            // e.g. "Unemployment rate: 4.2% as of 2026-08-01 (FRED UNRATE, fred)."
            Text(candidate.method).font(.subheadline).textSelection(.enabled)
            SourceCaption(text: "FRED · nightly batch")
            Text("Backdrop for pricing and valuation — not a trade signal.")
                .font(.caption2).foregroundStyle(.secondary)
        }.padding(.vertical, 4)
    }
}

private struct OutcomesBody: View {
    let payload: NightlyOutcomes

    var body: some View {
        let paper = payload.paperOutcomeSummary
        let sheets = payload.yellowSheets
        let entries = paper?.entryCount ?? 0
        let sheetCount = sheets?.sheetCount ?? 0

        LabeledContent("Paper outcomes observed", value: "\(entries)")
        if entries == 0 {
            Text("No paper outcomes recorded yet. An empty tally is reported as empty — never filled in.")
                .font(.caption).foregroundStyle(.secondary)
        } else if let counts = paper?.outcomeCounts, !counts.isEmpty {
            ForEach(counts.keys.sorted(), id: \.self) { key in
                LabeledContent(readable(key), value: "\(counts[key] ?? 0)")
                    .font(.subheadline)
            }
        }
        LabeledContent("Yellow sheets", value: "\(sheetCount)")
        if let decisions = sheets?.byDecision, !decisions.isEmpty {
            ForEach(decisions.keys.sorted(), id: \.self) { key in
                LabeledContent(readable(key), value: "\(decisions[key] ?? 0)")
                    .font(.subheadline)
            }
        }
        if let note = paper?.note {
            Text(note).font(.caption).foregroundStyle(.secondary)
        }
        SourceCaption(text: "paper-outcomes.jsonl + yellow-sheets.jsonl · nightly batch")
        Text("Observed results, not a forecast. No P&L claimed.")
            .font(.caption2).foregroundStyle(.secondary)
    }
}

private struct ApiSettingsView: View {
    @ObservedObject var store: TodayStore
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Form {
                Section("Hedge-desk server") {
                    TextField("Server address", text: $store.apiBaseURL)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                        .keyboardType(.URL)
                    Text("Default http://localhost:8765 works in the Simulator on the same Mac as the server. On a physical iPhone, use your Mac's address, e.g. http://192.168.1.20:8765.")
                        .font(.caption).foregroundStyle(.secondary)
                }
                Section {
                    Button("Reset to default") { store.apiBaseURL = defaultApiBaseURL }
                }
                Section {
                    Button("Save & Reload") {
                        dismiss()
                        Task { await store.refresh() }
                    }
                }
                Section {
                    Text("The app only reads research from your own paper-only server. It never places orders. Plain-http addresses on a local network can be blocked by iOS on a physical device; the Simulator on the server's Mac works out of the box.")
                        .font(.footnote).foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Server Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
            }
        }
    }
}
