import Foundation
import SwiftUI

struct DeskEnvelope: Decodable {
    let schema_version: String
    let report: DeskReport
    let morning_markdown: String
}
struct DeskReport: Decodable {
    let generated_at: String
    let environment: String
    let complete: Bool
    let live_orders_enabled: Bool
    let real_money_pnl: String
    let real_trades_executed: Int
    let report_sha256: String
    let projects: [ResearchDesk]
    let limitations: [String]
}
struct ResearchDesk: Decodable, Identifiable {
    var id: String { project_id }
    let project_id: String
    let evaluated_at: String
    let disposition: String
    let layers: [ControlLayer]
    var name: String {
        ["overnight-premium-desk": "Overnight Premium", "earnings-event-desk": "Earnings Event",
         "arbitrage-observer": "Box / Parity Observer", "dividend-opportunity-desk": "Dividend Opportunity",
         "open-quant-ai-model-lab": "Quant / AI Model Lab", "event-futures-desk": "Futures Event"][id] ?? readable(id)
    }
}
struct ControlLayer: Decodable, Identifiable {
    var id: String { layer }
    let layer: String
    let status: String
    let reason_codes: [String]
    let metrics: [String: String]
    let artifact_refs: [String]
    var name: String {
        ["OBSERVED": "Observed data", "STAT": "Statistical evidence", "BIG": "Research proposal",
         "DETERMINISTIC_RISK": "Deterministic risk", "DETERMINISTIC_COMPLIANCE": "Compliance", "HUMAN": "Human review"][layer] ?? readable(layer)
    }
}
struct Scenario: Identifiable {
    let id: String
    let group: String
    let disposition: String
    let reasons: [String]
    let details: String
}
struct ResearchNote: Codable, Identifiable {
    let id: UUID
    let createdAt: Date
    let desk: String
    let thesis: String
    let evidence: String
    let invalidation: String
    let reportHash: String
}
func readable(_ value: String) -> String {
    value.replacingOccurrences(of: "_", with: " ").replacingOccurrences(of: "-", with: " ").capitalized
}

@MainActor
final class ReportStore: ObservableObject {
    @Published var envelope: DeskEnvelope?
    @Published var scenarios: [Scenario] = []
    @Published var notes: [ResearchNote] = []
    @Published var loading = false
    @Published var error: String?
    @Published var source = "Bundled reference snapshot"
    @Published var rawReport = ""
    @Published var notesError: String?
    private let reportURL = URL(string: "https://trade-desk-research.boltonmd13.chatgpt.site/report.json")!
    private var notesURL: URL {
        FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("TradeDesk", isDirectory: true).appendingPathComponent("yellow-sheets.json")
    }
    init() {
        do {
            guard let url = Bundle.main.url(forResource: "report", withExtension: "json") else {
                throw ReportError.invalid("Bundled report is missing.")
            }
            try accept(Data(contentsOf: url))
        } catch { self.error = error.localizedDescription }
        do {
            if FileManager.default.fileExists(atPath: notesURL.path) {
                notes = try JSONDecoder().decode([ResearchNote].self, from: Data(contentsOf: notesURL))
            }
        } catch { notesError = "Saved notes could not be read. Existing notes will not be overwritten." }
    }
    private func accept(_ data: Data) throws {
        guard data.count <= 2_000_000 else { throw ReportError.invalid("Report exceeds the supported size.") }
        let decoded = try JSONDecoder().decode(DeskEnvelope.self, from: data)
        let report = decoded.report
        let expected: Set<String> = ["overnight-premium-desk", "earnings-event-desk", "arbitrage-observer", "dividend-opportunity-desk", "open-quant-ai-model-lab", "event-futures-desk"]
        guard decoded.schema_version == "desk-console-1", report.environment == "paper",
              report.complete, !report.live_orders_enabled, report.real_money_pnl == "0",
              report.real_trades_executed == 0, report.projects.count == expected.count,
              Set(report.projects.map(\.id)) == expected,
              report.projects.allSatisfy({ ["NO_TRADE", "HUMAN_REVIEW"].contains($0.disposition) }) else {
            throw ReportError.invalid("Unsupported report or paper-only boundary. No new decisions were loaded.")
        }
        guard let root = try JSONSerialization.jsonObject(with: data) as? [String: Any],
              let raw = root["report"] as? [String: Any],
              let games = raw["war_games"] as? [String: Any],
              let stress = raw["portfolio_stress"] as? [String: Any] else {
            throw ReportError.invalid("The report is missing scenario evidence.")
        }
        var rows: [Scenario] = []
        var groups = games
        groups["portfolio_stress"] = stress["scenarios"]
        for group in groups.keys.sorted() {
            guard let entries = groups[group] as? [[String: Any]] else { continue }
            for entry in entries {
                guard let id = entry["scenario_id"] as? String else { continue }
                let json = try JSONSerialization.data(withJSONObject: entry, options: [.prettyPrinted, .sortedKeys])
                rows.append(Scenario(id: group + ":" + id, group: group,
                    disposition: entry["disposition"] as? String ?? entry["lifecycle_action"] as? String ?? "REFERENCE_RESULT",
                    reasons: entry["reason_codes"] as? [String] ?? [], details: String(decoding: json, as: UTF8.self)))
            }
        }
        let json = try JSONSerialization.data(withJSONObject: raw, options: [.prettyPrinted, .sortedKeys])
        // Publish all display state only after complete parsing; no financial values are calculated here.
        envelope = decoded
        scenarios = rows
        rawReport = String(decoding: json, as: UTF8.self)
    }
    func refresh() async {
        guard !loading else { return }
        loading = true
        defer { loading = false }
        do {
            var request = URLRequest(url: reportURL)
            request.timeoutInterval = 20
            request.cachePolicy = .reloadIgnoringLocalCacheData
            let (data, response) = try await URLSession.shared.data(for: request)
            guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
                throw ReportError.invalid("The published report is unavailable. The previous snapshot remains displayed.")
            }
            try accept(data)
            source = "Published snapshot"
            error = nil
        } catch {
            self.error = "Refresh failed. Showing the previous snapshot. " + error.localizedDescription
        }
    }
    func addNote(desk: String, thesis: String, evidence: String, invalidation: String) throws {
        guard notesError == nil else { throw ReportError.invalid(notesError!) }
        guard let report = envelope?.report else { throw ReportError.invalid("A report is required.") }
        guard [thesis, evidence, invalidation].allSatisfy({ !$0.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty && $0.count <= 6000 }) else {
            throw ReportError.invalid("Complete each field using no more than 6,000 characters.")
        }
        let note = ResearchNote(id: UUID(), createdAt: Date(), desk: desk, thesis: thesis, evidence: evidence,
                                invalidation: invalidation, reportHash: report.report_sha256)
        let next = notes + [note]
        let bytes = try JSONEncoder().encode(next)
        try FileManager.default.createDirectory(at: notesURL.deletingLastPathComponent(), withIntermediateDirectories: true)
        try bytes.write(to: notesURL, options: .atomic)
        notes = next
    }
    var notesExport: String {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        encoder.dateEncodingStrategy = .iso8601
        guard let data = try? encoder.encode(notes) else { return "[]" }
        return String(decoding: data, as: UTF8.self)
    }
}
enum ReportError: LocalizedError {
    case invalid(String)
    var errorDescription: String? { if case let .invalid(message) = self { return message }; return nil }
}
