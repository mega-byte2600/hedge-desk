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
                ReportInfo().tabItem { Label("Report", systemImage: "doc.text.magnifyingglass") }
            }
            .tint(Color(red: 0.29, green: 0.48, blue: 0.23))
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
            Label("PAPER RESEARCH", systemImage: "shield.lefthalf.filled").font(.caption.weight(.bold))
            Text("Synthetic fixtures. No live orders.").font(.subheadline)
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
                if let report = store.envelope?.report {
                    Section("Research desks") {
                        ForEach(report.projects) { desk in
                            NavigationLink {
                                DeskDetail(desk: desk)
                            } label: {
                                VStack(alignment: .leading, spacing: 10) {
                                    Text(desk.name).font(.headline)
                                    StatusBadge(value: desk.disposition)
                                }.padding(.vertical, 6)
                            }
                        }
                    }
                } else {
                    Text("No report available. Pull down to retry.")
                }
            }
            .navigationTitle("Trade Desk")
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
struct ReportInfo: View {
    @EnvironmentObject var store: ReportStore
    var body: some View {
        NavigationStack {
            List {
                Section { SnapshotBanner() }
                if let envelope = store.envelope {
                    Section("Snapshot identity") {
                        LabeledContent("Exported", value: envelope.report.generated_at)
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
                    Link("Open website", destination: URL(string: "https://trade-desk-research.boltonmd13.chatgpt.site")!)
                    Link("GitHub repository", destination: URL(string: "https://github.com/mega-byte2600/hedge-desk")!)
                    Text("Refresh downloads the published snapshot; it does not run the Python engine. Bundled data is available offline. This app performs no trading or financial calculations.")
                        .font(.footnote).foregroundStyle(.secondary)
                }
            }.navigationTitle("Report")
        }
    }
}
