import SwiftUI

@main
struct TradeDeskApp: App {
    @StateObject private var store = ReportStore()
    var body: some Scene {
        WindowGroup {
            TabView {
                DeskList().tabItem { Label("Desks", systemImage: "square.grid.2x2") }
                ScenarioList().tabItem { Label("Scenarios", systemImage: "waveform.path.ecg") }
                NotesList().tabItem { Label("Yellow Sheets", systemImage: "note.text") }
                ResourcesList().tabItem { Label("Resources", systemImage: "books.vertical") }
                ReportInfo().tabItem { Label("Report", systemImage: "doc.text.magnifyingglass") }
            }
            .environmentObject(store)
        }
    }
}
struct StatusBadge: View {
    let value: String
    var color: Color {
        if value.contains("BLOCK") || value == "NO_TRADE" || value.contains("FREEZE") { return .red }
        if value.contains("REVIEW") || value == "PENDING" { return .orange }
        if value == "PASS" { return .green }
        return .secondary
    }
    var body: some View {
        Text(readable(value)).font(.caption.weight(.semibold)).foregroundStyle(color)
            .padding(.horizontal, 8).padding(.vertical, 5).background(color.opacity(0.1), in: RoundedRectangle(cornerRadius: 5))
    }
}
struct SnapshotBanner: View {
    @EnvironmentObject var store: ReportStore
    var body: some View {
        VStack(alignment: .leading, spacing: 7) {
            Label("EMPORION · RESEARCH PLATFORM", systemImage: "shield.lefthalf.filled").font(.caption.weight(.bold))
            Text("Markets · Intelligence · Discipline").font(.subheadline.weight(.semibold))
            Text("Seven research desks · Six evaluated workflows").font(.caption).foregroundStyle(.secondary)
            Text("Paper research by default. No live orders.").font(.caption).foregroundStyle(.secondary)
            Text(store.source).font(.caption).foregroundStyle(.secondary)
            if let error = store.error { Text(error).font(.caption).foregroundStyle(.red) }
        }.padding(.vertical, 5)
    }
}
struct DeskList: View {
    @EnvironmentObject var store: ReportStore
    var body: some View {
        NavigationStack {
            List {
                Section { SnapshotBanner() }
                if let envelope = store.envelope {
                    Section("Research desks") {
                        ForEach(envelope.registry.sorted(by: { $0.number < $1.number })) { registryDesk in
                            if let desk = envelope.report.projects.first(where: { $0.id == registryDesk.id }) {
                                NavigationLink {
                                    DeskDetail(desk: desk)
                                } label: {
                                    VStack(alignment: .leading, spacing: 7) {
                                        Text(String(format: "Desk %02d", registryDesk.number)).font(.caption).foregroundStyle(.secondary)
                                        Text(registryDesk.name).font(.headline)
                                        StatusBadge(value: desk.disposition)
                                    }.padding(.vertical, 5)
                                }
                            } else {
                                VStack(alignment: .leading, spacing: 7) {
                                    Text(String(format: "Desk %02d", registryDesk.number)).font(.caption).foregroundStyle(.secondary)
                                    Text(registryDesk.name).font(.headline)
                                    Text(registryDesk.objective).font(.caption).foregroundStyle(.secondary)
                                    StatusBadge(value: "ARCHITECTURE ONLY")
                                }.padding(.vertical, 5)
                            }
                        }
                    }
                } else {
                    Text("No report available. Pull down to retry.")
                }
            }
            .navigationTitle("Emporion")
            .refreshable { await store.refresh() }
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button { Task { await store.refresh() } } label: {
                        if store.loading { ProgressView() } else { Image(systemName: "arrow.clockwise") }
                    }.disabled(store.loading).accessibilityLabel("Reload published snapshot")
                }
            }
        }
    }
}
struct DeskDetail: View {
    let desk: ResearchDesk
    var body: some View {
        List {
            Section {
                StatusBadge(value: desk.disposition)
                LabeledContent("Fixture evaluated", value: desk.evaluated_at)
                Text("Reference snapshot, not a current market signal.").font(.caption).foregroundStyle(.secondary)
            }
            ForEach(desk.layers) { layer in
                Section(layer.name) {
                    StatusBadge(value: layer.status)
                    ForEach(layer.reason_codes, id: \.self) { reason in
                        Text(reason).font(.caption.monospaced()).foregroundStyle(.red).textSelection(.enabled)
                    }
                    ForEach(layer.metrics.keys.sorted(), id: \.self) { key in
                        VStack(alignment: .leading, spacing: 5) {
                            Text(readable(key)).font(.caption).foregroundStyle(.secondary)
                            Text(layer.metrics[key] ?? "").font(.subheadline.monospaced()).textSelection(.enabled)
                        }
                    }
                    if !layer.artifact_refs.isEmpty {
                        DisclosureGroup("Evidence references") {
                            ForEach(Array(layer.artifact_refs.enumerated()), id: \.offset) { _, reference in
                                Text(reference).font(.caption.monospaced()).textSelection(.enabled)
                            }
                        }
                    }
                }
            }
            Section {
                Text("Risk values are recorded outputs of the existing engine. The reference RoR model is unvalidated. This app does not calculate RoR, approve trades, or override controls.")
                    .font(.footnote).foregroundStyle(.secondary)
            }
        }.navigationTitle(desk.name).navigationBarTitleDisplayMode(.inline)
    }
}
struct ScenarioList: View {
    @EnvironmentObject var store: ReportStore
    @State private var query = ""
    @State private var blockedOnly = false
    var filtered: [Scenario] {
        store.scenarios.filter {
            (!blockedOnly || $0.disposition == "NO_TRADE" || $0.disposition == "FREEZE_NEW_RISK") &&
            (query.isEmpty || ($0.id + " " + $0.reasons.joined(separator: " ")).localizedCaseInsensitiveContains(query))
        }
    }
    var body: some View {
        NavigationStack {
            List {
                Section {
                    Toggle("No-trade and freeze cases only", isOn: $blockedOnly)
                    Text("\(filtered.count) scenario records · synthetic fixtures").font(.caption).foregroundStyle(.secondary)
                }
                ForEach(filtered) { scenario in
                    NavigationLink {
                        ScrollView {
                            VStack(alignment: .leading, spacing: 16) {
                                StatusBadge(value: scenario.disposition)
                                Text("Exact engine record. Synthetic fixture only.").font(.footnote).foregroundStyle(.secondary)
                                Text(scenario.details).font(.caption.monospaced()).textSelection(.enabled)
                            }.padding().frame(maxWidth: .infinity, alignment: .leading)
                        }.navigationTitle("Scenario evidence").navigationBarTitleDisplayMode(.inline)
                    } label: {
                        VStack(alignment: .leading, spacing: 7) {
                            Text(readable(String(scenario.id.split(separator: ":").last ?? ""))).font(.headline)
                            Text(readable(scenario.group)).font(.caption).foregroundStyle(.secondary)
                            StatusBadge(value: scenario.disposition)
                        }.padding(.vertical, 5)
                    }
                }
                if filtered.isEmpty { Text("No scenarios match your search.").foregroundStyle(.secondary) }
            }.navigationTitle("Scenario Lab").searchable(text: $query, prompt: "Scenario or reason code")
        }
    }
}
struct NotesList: View {
    @EnvironmentObject var store: ReportStore
    @State private var compose = false
    var body: some View {
        NavigationStack {
            List {
                Section {
                    Text("Research notes stay on this iPhone. Export a copy before deleting the app. Notes do not authorize trades.")
                        .font(.footnote).foregroundStyle(.secondary)
                    if let error = store.notesError { Text(error).foregroundStyle(.red) }
                }
                ForEach(store.notes.reversed()) { note in
                    NavigationLink {
                        List {
                            Section("Thesis") { Text(note.thesis).textSelection(.enabled) }
                            Section("Evidence") { Text(note.evidence).textSelection(.enabled) }
                            Section("What would invalidate it?") { Text(note.invalidation).textSelection(.enabled) }
                            Section("Report SHA-256") { Text(note.reportHash).font(.caption.monospaced()).textSelection(.enabled) }
                        }.navigationTitle(readable(note.desk)).navigationBarTitleDisplayMode(.inline)
                    } label: {
                        VStack(alignment: .leading, spacing: 7) {
                            Text(readable(note.desk)).font(.caption).foregroundStyle(.secondary)
                            Text(note.thesis).lineLimit(3)
                            Text(note.createdAt, style: .date).font(.caption).foregroundStyle(.secondary)
                        }
                    }
                }
                if store.notes.isEmpty { Text("Start your first Yellow Sheet with +.").foregroundStyle(.secondary) }
            }.navigationTitle("Yellow Sheets")
                .toolbar {
                    ToolbarItem(placement: .navigationBarLeading) { ShareLink(item: store.notesExport) { Image(systemName: "square.and.arrow.up") }.accessibilityLabel("Export notes") }
                    ToolbarItem(placement: .navigationBarTrailing) { Button { compose = true } label: { Image(systemName: "plus") }.disabled(store.envelope == nil || store.notesError != nil).accessibilityLabel("New research note") }
                }
                .sheet(isPresented: $compose) { NoteEditor() }
        }
    }
}
struct NoteEditor: View {
    @EnvironmentObject var store: ReportStore
    @Environment(\.dismiss) var dismiss
    @State private var desk = "overnight-premium-desk"
    @State private var thesis = ""
    @State private var evidence = ""
    @State private var invalidation = ""
    @State private var error: String?
    var complete: Bool { [thesis, evidence, invalidation].allSatisfy { !$0.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty && $0.count <= 6000 } }
    var body: some View {
        NavigationStack {
            Form {
                Picker("Desk", selection: $desk) { ForEach(store.envelope?.report.projects ?? []) { Text($0.name).tag($0.id) } }
                Section("Thesis") { TextEditor(text: $thesis).frame(minHeight: 100).accessibilityLabel("Thesis") }
                Section("Evidence") { TextEditor(text: $evidence).frame(minHeight: 100).accessibilityLabel("Evidence") }
                Section("What would invalidate it?") { TextEditor(text: $invalidation).frame(minHeight: 100).accessibilityLabel("Invalidation conditions") }
                Section { Text("Maximum 6,000 characters per field. Bound to the current report.").font(.caption) }
                if let error = error { Text(error).foregroundStyle(.red) }
            }.navigationTitle("New Yellow Sheet").navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) { Button("Cancel") { dismiss() } }
                    ToolbarItem(placement: .confirmationAction) {
                        Button("Save") {
                            do { try store.addNote(desk: desk, thesis: thesis, evidence: evidence, invalidation: invalidation); dismiss() }
                            catch { self.error = error.localizedDescription }
                        }.disabled(!complete)
                    }
                }
        }.interactiveDismissDisabled(!thesis.isEmpty || !evidence.isEmpty || !invalidation.isEmpty)
    }
}

struct ResearchResource: Identifiable {
    let id: String
    let name: String
    let url: URL
    let description: String
}

struct ResearchResourceGroup: Identifiable {
    let id: String
    let title: String
    let note: String
    let resources: [ResearchResource]
}

private let researchResourceGroups: [ResearchResourceGroup] = [
    ResearchResourceGroup(
        id: "rates-bonds-policy",
        title: "Rates, Bonds & Monetary Policy",
        note: "Primary institutional sources first.",
        resources: [
            ResearchResource(id: "ny-fed-reference-rates", name: "New York Fed · Reference Rates", url: URL(string: "https://www.newyorkfed.org/markets/reference-rates")!, description: "SOFR, EFFR, repo reference rates, money-market plumbing, and monetary-policy implementation."),
            ResearchResource(id: "treasury-rates", name: "U.S. Treasury · Interest Rate Statistics", url: URL(string: "https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics")!, description: "Official Treasury par yield curves, real yield curves, bill rates, and related rate statistics."),
            ResearchResource(id: "fed-policy", name: "Federal Reserve Board · Monetary Policy", url: URL(string: "https://www.federalreserve.gov/monetarypolicy.htm")!, description: "FOMC policy statements, implementation information, reports, and official Federal Reserve policy materials."),
            ResearchResource(id: "fred", name: "FRED · Federal Reserve Bank of St. Louis", url: URL(string: "https://fred.stlouisfed.org/")!, description: "Macro, rates, credit, inflation, employment, and financial-market time series."),
            ResearchResource(id: "finra-fixed-income", name: "FINRA · Fixed Income Data", url: URL(string: "https://www.finra.org/finra-data/fixed-income")!, description: "TRACE and other fixed-income market data for corporate and agency debt research."),
            ResearchResource(id: "cme-rates", name: "CME Group · Interest Rates", url: URL(string: "https://www.cmegroup.com/markets/interest-rates.html")!, description: "Treasury, SOFR, Fed Funds, and other listed interest-rate futures and options.")
        ]
    ),
    ResearchResourceGroup(
        id: "filings-earnings-fundamentals",
        title: "Filings, Earnings & Fundamental Research",
        note: "Primary filings and event research.",
        resources: [
            ResearchResource(id: "sec-edgar", name: "SEC · EDGAR", url: URL(string: "https://www.sec.gov/search-filings")!, description: "Official U.S. public-company filings, registration statements, ownership forms, and filing search."),
            ResearchResource(id: "earnings-whispers", name: "Earnings Whispers", url: URL(string: "https://www.earningswhispers.com/")!, description: "Earnings calendars, reported results, and expectation-focused event research."),
            ResearchResource(id: "finviz", name: "Finviz", url: URL(string: "https://finviz.com/")!, description: "Screening, market maps, fundamentals, technical context, and news discovery.")
        ]
    ),
    ResearchResourceGroup(
        id: "macro-derivatives-market-structure",
        title: "Macro, Derivatives & Market Structure",
        note: "Official statistics and exchange-level market context.",
        resources: [
            ResearchResource(id: "bls", name: "BLS · U.S. Bureau of Labor Statistics", url: URL(string: "https://www.bls.gov/")!, description: "Official employment, CPI, PPI, productivity, and labor-market statistics."),
            ResearchResource(id: "bea", name: "BEA · U.S. Bureau of Economic Analysis", url: URL(string: "https://www.bea.gov/")!, description: "Official GDP, personal income, consumption, trade, and national accounts."),
            ResearchResource(id: "cboe", name: "Cboe Global Markets", url: URL(string: "https://www.cboe.com/")!, description: "Options, volatility, index, and market-structure resources.")
        ]
    )
]

struct ResourcesList: View {
    var body: some View {
        NavigationStack {
            List {
                Section {
                    VStack(alignment: .leading, spacing: 7) {
                        Label("PRIMARY-SOURCE FIRST", systemImage: "building.columns").font(.caption.weight(.bold))
                        Text("Open public research sources directly for rates, bonds, policy, filings, macro data, earnings, derivatives, and market structure.")
                            .font(.footnote).foregroundStyle(.secondary)
                    }.padding(.vertical, 4)
                }
                ForEach(researchResourceGroups) { group in
                    Section {
                        ForEach(group.resources) { resource in
                            Link(destination: resource.url) {
                                VStack(alignment: .leading, spacing: 5) {
                                    HStack {
                                        Text(resource.name).font(.headline).foregroundStyle(.primary)
                                        Spacer()
                                        Image(systemName: "arrow.up.right.square").foregroundStyle(.secondary)
                                    }
                                    Text(resource.description).font(.caption).foregroundStyle(.secondary)
                                }.padding(.vertical, 4)
                            }
                            .accessibilityHint("Opens the official external research source")
                        }
                    } header: {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(group.title)
                            Text(group.note).font(.caption2).textCase(nil)
                        }
                    }
                }
                Section {
                    Text("External resources are provided for research convenience. Inclusion does not imply affiliation, endorsement, sponsorship, investment advice, or trade authorization.")
                        .font(.footnote).foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Research Resources")
        }
    }
}

struct ReportInfo: View {
    @EnvironmentObject var store: ReportStore
    var body: some View {
        NavigationStack {
            List {
                Section { SnapshotBanner() }
                if let envelope = store.envelope {
                    Section("Snapshot identity") {
                        LabeledContent("Exported", value: envelope.report.generated_at)
                        LabeledContent("Research desks", value: String(envelope.registry.count))
                        LabeledContent("Evaluated workflows", value: String(envelope.report.projects.count))
                        LabeledContent("Real trades", value: String(envelope.report.real_trades_executed))
                        LabeledContent("Live orders", value: "Disabled")
                        Text(envelope.report.report_sha256).font(.caption.monospaced()).textSelection(.enabled)
                    }
                    Section("Export") {
                        ShareLink(item: envelope.morning_markdown) { Label("Share morning packet", systemImage: "square.and.arrow.up") }
                        ShareLink(item: store.rawReport) { Label("Share report JSON", systemImage: "doc.text") }
                    }
                    Section("Research limitations") { ForEach(envelope.report.limitations, id: \.self) { Text($0).font(.footnote) } }
                }
                Section {
                    Link("Open Emporion website", destination: URL(string: "https://hedge-desk.onrender.com")!)
                    Link("GitHub repository", destination: URL(string: "https://github.com/mega-byte2600/hedge-desk")!)
                    Text("Refresh downloads the published snapshot; it does not run the Python engine. Bundled data is available offline. This app performs no trading or financial calculations.")
                        .font(.footnote).foregroundStyle(.secondary)
                }
            }.navigationTitle("Emporion Report")
        }
    }
}
