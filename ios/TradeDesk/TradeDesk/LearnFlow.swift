import SwiftUI

// MARK: - Learn: "How the desk makes money" walkthrough
//
// Phone-first onboarding for someone who has never sold an option.
// Every number marked ILLUSTRATIVE is a teaching figure, not a market quote.

struct LearnHome: View {
    var body: some View {
        NavigationStack {
            List {
                Section {
                    VStack(alignment: .leading, spacing: 8) {
                        Label("START HERE", systemImage: "graduationcap")
                            .font(.caption.weight(.bold))
                            .foregroundColor(.accentColor)
                        Text("How selling premium pays")
                            .font(.title2.weight(.bold))
                        Text("Six short chapters. About five minutes. No finance background needed — each idea gets a one-line plain-English version first.")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding(.vertical, 6)
                }
                Section("Chapters") {
                    LearnRow(number: 1, title: "The insurance idea", subtitle: "Selling puts, in one sentence", destination: LearnChapter1())
                    LearnRow(number: 2, title: "Anatomy of one trade", subtitle: "Four steps and a worked example", destination: LearnChapter2())
                    LearnRow(number: 3, title: "The three doors at expiry", subtitle: "What can actually happen", destination: LearnChapter3())
                    LearnRow(number: 4, title: "Why the math favors sellers", subtitle: "Time decay and the honesty clause", destination: LearnChapter4())
                    LearnRow(number: 5, title: "Best contracts right now", subtitle: "The desk's scorecard", destination: LearnChapter5())
                    LearnRow(number: 6, title: "How the desk runs it", subtitle: "Research to paper, step by step", destination: LearnChapter6())
                }
                Section {
                    Text("Paper-only education. Nothing here is a trade recommendation, and research is input — not performance, not income.")
                        .font(.footnote)
                        .foregroundColor(.secondary)
                }
            }
            .navigationTitle("Learn")
        }
    }
}

private struct LearnRow<Destination: View>: View {
    let number: Int
    let title: String
    let subtitle: String
    let destination: Destination
    var body: some View {
        NavigationLink {
            destination
        } label: {
            HStack(spacing: 12) {
                Text("\(number)")
                    .font(.headline.weight(.bold))
                    .foregroundColor(.white)
                    .frame(width: 30, height: 30)
                    .background(Color.accentColor, in: Circle())
                VStack(alignment: .leading, spacing: 2) {
                    Text(title).font(.headline)
                    Text(subtitle).font(.caption).foregroundColor(.secondary)
                }
            }
            .padding(.vertical, 4)
        }
    }
}

// MARK: - Shared pieces

struct LearnCard<Content: View>: View {
    let title: String
    let systemImage: String
    let accent: Color
    let content: Content
    init(title: String, systemImage: String, accent: Color = .accentColor, @ViewBuilder content: () -> Content) {
        self.title = title
        self.systemImage = systemImage
        self.accent = accent
        self.content = content()
    }
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Label(title, systemImage: systemImage)
                .font(.headline)
                .foregroundColor(accent)
            content
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(14)
    }
}

struct LearnStep: View {
    let number: Int
    let title: String
    let body: String
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Text("\(number)")
                .font(.subheadline.weight(.bold))
                .foregroundColor(.white)
                .frame(width: 26, height: 26)
                .background(Color.accentColor, in: Circle())
            VStack(alignment: .leading, spacing: 4) {
                Text(title).font(.subheadline.weight(.semibold))
                Text(body).font(.subheadline).foregroundColor(.secondary)
            }
        }
    }
}

struct ChapterShell<Content: View>: View {
    let kicker: String
    let title: String
    let content: Content
    init(kicker: String, title: String, @ViewBuilder content: () -> Content) {
        self.kicker = kicker
        self.title = title
        self.content = content()
    }
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                VStack(alignment: .leading, spacing: 6) {
                    Text(kicker.uppercased())
                        .font(.caption.weight(.bold))
                        .foregroundColor(.accentColor)
                    Text(title)
                        .font(.title.weight(.bold))
                }
                content
            }
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Chapter 1: The insurance idea

struct LearnChapter1: View {
    var body: some View {
        ChapterShell(kicker: "Chapter 1", title: "The insurance idea") {
            LearnCard(title: "One sentence", systemImage: "lightbulb") {
                Text("We sell insurance on stocks. Buyers pay us up front for the right to sell us shares at a set price — most of the time they never use it, and we keep the money.")
                    .font(.body)
            }
            LearnCard(title: "The two sides", systemImage: "person.2") {
                VStack(alignment: .leading, spacing: 10) {
                    HStack(alignment: .top, spacing: 8) {
                        Image(systemName: "arrow.up.right").foregroundColor(.red)
                        VStack(alignment: .leading, spacing: 2) {
                            Text("The buyer").font(.subheadline.weight(.semibold))
                            Text("Pays for protection against a fall. Like car insurance — hopes to never use it.").font(.subheadline).foregroundColor(.secondary)
                        }
                    }
                    HStack(alignment: .top, spacing: 8) {
                        Image(systemName: "arrow.down.right").foregroundColor(.green)
                        VStack(alignment: .leading, spacing: 2) {
                            Text("The seller (us)").font(.subheadline.weight(.semibold))
                            Text("Collects the payment on day one. Keeps it when nothing bad happens — which is most of the time.").font(.subheadline).foregroundColor(.secondary)
                        }
                    }
                }
            }
            LearnCard(title: "The contract: a cash-secured put", systemImage: "doc.text") {
                Text("A put gives its buyer the right to sell 100 shares to us at the strike price before expiry. \"Cash-secured\" means we set aside the full cash to buy those shares — no leverage, no margin calls.")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
    }
}

// MARK: - Chapter 2: Anatomy of one trade

struct LearnChapter2: View {
    var body: some View {
        ChapterShell(kicker: "Chapter 2", title: "Anatomy of one trade") {
            VStack(alignment: .leading, spacing: 14) {
                LearnStep(number: 1, title: "Pick the underlying and strike",
                          body: "A stock you'd be happy to own, strike about 10% below today's price, roughly 30–45 days out.")
                LearnStep(number: 2, title: "Sell the put, collect cash",
                          body: "The premium lands in the account on day one. Set aside the collateral to buy the shares if needed.")
                LearnStep(number: 3, title: "Let time decay work",
                          body: "Every day, time decay (theta) melts the option's value. That melt is your profit accruing.")
                LearnStep(number: 4, title: "Expiry arrives",
                          body: "Stock above the strike: keep it all. Below: you buy the shares at the strike — the price you already agreed was fine.")
            }
            LearnCard(title: "Worked example", systemImage: "calculator", accent: .green) {
                VStack(alignment: .leading, spacing: 8) {
                    LearnFactRow(label: "Stock XYZ", value: "$100")
                    LearnFactRow(label: "Strike sold", value: "$90 (10% below)")
                    LearnFactRow(label: "Days to expiry", value: "40")
                    LearnFactRow(label: "Premium collected", value: "$1.50 → $150 per contract")
                    LearnFactRow(label: "Collateral set aside", value: "$9,000")
                    Divider()
                    LearnFactRow(label: "Max gain", value: "$150 — a 1.67% return on collateral in ~40 days")
                    LearnFactRow(label: "Breakeven at expiry", value: "$88.50")
                    Text("Illustrative example, not a real quote. Real premiums come from the live option chain.")
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .padding(.top, 4)
                }
            }
        }
    }
}

struct LearnFactRow: View {
    let label: String
    let value: String
    var body: some View {
        HStack(alignment: .top) {
            Text(label).font(.subheadline).foregroundColor(.secondary)
            Spacer()
            Text(value).font(.subheadline.weight(.semibold)).multilineTextAlignment(.trailing)
        }
    }
}

// MARK: - Chapter 3: The three doors at expiry

struct LearnChapter3: View {
    enum Door: Int, CaseIterable {
        case above, below, early
        var title: String {
            switch self {
            case .above: return "Above the strike"
            case .below: return "Below the strike"
            case .early: return "Buy back early"
            }
        }
    }
    @State private var door: Door = .above
    var body: some View {
        ChapterShell(kicker: "Chapter 3", title: "The three doors at expiry") {
            Text("Only three things can happen. Tap each door.")
                .font(.subheadline)
                .foregroundColor(.secondary)
            Picker("Outcome", selection: $door) {
                ForEach(Door.allCases, id: \.self) { d in
                    Text(d.title).tag(d)
                }
            }
            .pickerStyle(.segmented)
            Group {
                switch door {
                case .above:
                    LearnCard(title: "Door 1 — stock closes above $90", systemImage: "door.left.hand.open", accent: .green) {
                        Text("The put expires worthless. You keep the full $150. This is the most common door — the strike was set 10% below the price for a reason.")
                            .font(.subheadline)
                    }
                case .below:
                    LearnCard(title: "Door 2 — stock closes below $90", systemImage: "door.right.hand.open", accent: .orange) {
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Assignment: you buy 100 shares at $90 — the price you already decided was fine when you sold the put.")
                                .font(.subheadline)
                            Text("This is why the desk only sells puts on names it would own anyway. Assignment isn't failure; it's buying the stock at your chosen discount.")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    }
                case .early:
                    LearnCard(title: "Door 3 — buy it back early", systemImage: "arrow.uturn.backward", accent: .blue) {
                        Text("If the put's value melted to $0.40 with two weeks left, buy it back, lock in most of the profit, and free the $9,000 collateral for the next trade. You don't have to wait for expiry.")
                            .font(.subheadline)
                    }
                }
            }
            .animation(.easeInOut, value: door)
        }
    }
}

// MARK: - Chapter 4: Why the math favors sellers

struct ThetaChart: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            GeometryReader { geo in
                let w = geo.size.width
                let h = geo.size.height
                let leftPad: CGFloat = 6
                let bottomPad: CGFloat = 6
                ZStack {
                    Path { p in
                        let n = 60
                        for i in 0...n {
                            let t = CGFloat(i) / CGFloat(n)
                            let dte = 45.0 * (1.0 - Double(t))
                            let value = pow(dte / 45.0, 1.6)
                            let x = leftPad + t * (w - leftPad - 6)
                            let y = (h - bottomPad) - CGFloat(value) * (h - bottomPad - 6)
                            if i == 0 { p.move(to: CGPoint(x: x, y: y)) }
                            else { p.addLine(to: CGPoint(x: x, y: y)) }
                        }
                    }
                    .stroke(Color.green, lineWidth: 3)
                    Path { p in
                        p.move(to: CGPoint(x: leftPad, y: h - bottomPad))
                        p.addLine(to: CGPoint(x: w - 6, y: h - bottomPad))
                    }
                    .stroke(Color.secondary.opacity(0.5), lineWidth: 1)
                }
            }
            .frame(height: 170)
            HStack {
                Text("45 days out").font(.caption).foregroundColor(.secondary)
                Spacer()
                Text("Expiry").font(.caption).foregroundColor(.secondary)
            }
        }
    }
}

struct LearnChapter4: View {
    var body: some View {
        ChapterShell(kicker: "Chapter 4", title: "Why the math favors sellers") {
            LearnCard(title: "Options rot — sellers collect the rot", systemImage: "chart.line.downtrend.xyaxis", accent: .green) {
                VStack(alignment: .leading, spacing: 10) {
                    Text("An option's time value melts a little every day, and the melting speeds up near expiry. As the seller, that melt is your profit accruing. The chart shows a typical 45-day decay curve.")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                    ThetaChart()
                }
            }
            LearnCard(title: "Buyers overpay for insurance", systemImage: "shield", accent: .blue) {
                Text("Implied volatility — what buyers pay for — usually runs hotter than the volatility that actually happens. The gap between the two is called the volatility risk premium, and put sellers harvest it, trade after trade.")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            LearnCard(title: "The honest catch", systemImage: "exclamationmark.triangle", accent: .orange) {
                VStack(alignment: .leading, spacing: 8) {
                    Text("Small wins, often. Rare losses, bigger. That is the trade — there is no version of it without the second half.")
                        .font(.subheadline.weight(.semibold))
                    Text("The desk survives it with position sizing: no single position may risk more than 2% of equity. One bad week is then an annoyance, not an ending.")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }
        }
    }
}

// MARK: - Chapter 5: Best contracts right now

struct UnderlyingScore: Identifiable {
    var id: String { ticker }
    let grade: String
    let ticker: String
    let name: String
    let note: String
}

struct GradeBadge: View {
    let grade: String
    var color: Color {
        if grade.hasPrefix("A") { return .green }
        if grade.hasPrefix("B") { return .blue }
        return .orange
    }
    var body: some View {
        Text(grade)
            .font(.headline.weight(.bold))
            .foregroundColor(.white)
            .frame(width: 44, height: 44)
            .background(color, in: RoundedRectangle(cornerRadius: 10))
    }
}

struct LearnChapter5: View {
    let scores: [UnderlyingScore] = [
        UnderlyingScore(grade: "A", ticker: "SPY", name: "S&P 500 ETF",
                        note: "The default. Broad diversification, tightest spreads, no earnings to dodge."),
        UnderlyingScore(grade: "A", ticker: "QQQ", name: "Nasdaq 100 ETF",
                        note: "Same playbook with a tech tilt. No earnings, deep liquidity."),
        UnderlyingScore(grade: "B", ticker: "MSFT", name: "Microsoft",
                        note: "Liquid mega-cap — but earnings Oct 27/28 fall inside a 30–45 day window. Wait it out or go shorter."),
        UnderlyingScore(grade: "B", ticker: "AAPL", name: "Apple",
                        note: "Same flag: earnings Oct 29 inside the window. Fine name, wrong week."),
        UnderlyingScore(grade: "B−", ticker: "NVDA", name: "Nvidia",
                        note: "Richer premiums, violent moves. Earnings Nov 25 are clear of the window — size small."),
        UnderlyingScore(grade: "C", ticker: "TSLA", name: "Tesla",
                        note: "Deliveries report ~Oct 2 is a binary event inside the window. Stand aside until it passes."),
    ]
    var body: some View {
        ChapterShell(kicker: "Chapter 5", title: "Best contracts right now") {
            LearnCard(title: "What makes a good underlying", systemImage: "checklist") {
                VStack(alignment: .leading, spacing: 6) {
                    Text("• Liquidity first — tight bid/ask spreads, heavy volume").font(.subheadline)
                    Text("• Diversification — an index can't gap on one CEO's tweet").font(.subheadline)
                    Text("• No binary event inside the window — earnings, FDA, deliveries").font(.subheadline)
                    Text("• Enough volatility to make the premium worth collecting").font(.subheadline)
                }
                .foregroundColor(.secondary)
            }
            ForEach(scores) { s in
                HStack(alignment: .top, spacing: 12) {
                    GradeBadge(grade: s.grade)
                    VStack(alignment: .leading, spacing: 4) {
                        HStack {
                            Text(s.ticker).font(.headline)
                            Text(s.name).font(.caption).foregroundColor(.secondary)
                        }
                        Text(s.note).font(.subheadline).foregroundColor(.secondary)
                    }
                }
                .padding()
                .background(Color(.secondarySystemBackground))
                .cornerRadius(14)
            }
            LearnCard(title: "Today's weather", systemImage: "cloud.sun", accent: .blue) {
                Text("VIX sits near 52-week lows (~15 at last close) — absolute premiums are thin right now. The edge persists, but the paychecks are smaller. As of Fri Sep 25 close; the desk re-scores this daily.")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
    }
}

// MARK: - Chapter 6: How the desk runs it

struct LearnChapter6: View {
    var body: some View {
        ChapterShell(kicker: "Chapter 6", title: "How the desk runs it") {
            Text("Six steps, every cycle. Research proposes — a human decides.")
                .font(.subheadline)
                .foregroundColor(.secondary)
            VStack(alignment: .leading, spacing: 14) {
                LearnStep(number: 1, title: "Nightly research",
                          body: "The research desk scans all six desks — premium, earnings, dividends, parity, quant, futures — and publishes findings.")
                LearnStep(number: 2, title: "Screen candidates",
                          body: "Liquidity, volatility rank, and the event calendar filter the list. Most ideas die here.")
                LearnStep(number: 3, title: "Risk gates",
                          body: "The 2% max-loss rule and deterministic checks run. No gate passed, no trade — no exceptions.")
                LearnStep(number: 4, title: "You decide",
                          body: "The GP steers. Nothing becomes a position without a human decision. This is the step you're standing in.")
                LearnStep(number: 5, title: "Paper tracked",
                          body: "Every approved plan is tracked on paper — entries, exits, and outcomes recorded either way.")
                LearnStep(number: 6, title: "Settler scores it",
                          body: "A read-only settler marks each plan against its own terms. Wins and losses both feed the next night's research.")
            }
            LearnCard(title: "Paper only", systemImage: "doc.badge.clock", accent: .blue) {
                Text("This desk runs on paper by design. The app shows research and tracks paper plans — it places no orders, holds no money, and never overrides a risk control.")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
    }
}
