/* overview-revamp.js — Hedge Desk overview revamp (prototype).
 *
 * Drop-in replacement for the app.js `overview()` render function.
 * Same data inputs: (data, report, brief?)
 *   data.summary        { desks_reporting, desks_total, scenarios, data_as_of }
 *   data.candidate_feed { candidates: [...] }
 *   data.registry       [{ project_id, name, objective }] (optional; used as method fallback)
 *   report.projects     [{ project_id, data_status, data_as_of, ... }]
 *   brief               { date, headline } (optional; from research-brief.json)
 *
 * Returns an HTML string. No dependencies, no DOM writes — the caller injects
 * the string wherever overview() output goes. Plain script (file:// safe);
 * the repo integrator can wrap it as an ES module if preferred.
 *
 * Copy budget: under 150 words of static copy on the whole page.
 */
(function (root) {
  'use strict';

  var DESK_NAMES = {
    'overnight-premium-desk': 'Overnight Premium',
    'earnings-event-desk': 'Earnings Event',
    'arbitrage-observer': 'Box / Parity Observer',
    'dividend-opportunity-desk': 'Dividend Opportunity',
    'open-quant-ai-model-lab': 'Quant / AI Model Lab',
    'event-futures-desk': 'Futures Event'
  };

  var DESK_METHODS = {
    'overnight-premium-desk': 'Premium capture with defined risk and spread checks.',
    'earnings-event-desk': 'Expected vs. reported results, and price reaction.',
    'arbitrage-observer': 'Parity and box relationships, net of costs.',
    'dividend-opportunity-desk': 'Payout durability: cash flow, yield, valuation.',
    'open-quant-ai-model-lab': 'Reproducible quant and model-signal research.',
    'event-futures-desk': 'Physical events read against futures curves.'
  };

  var STATUS_WORD = { live: 'Live', batch: 'Batch' };
  var FRESH_H = 6, STALE_H = 24;

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function fmtDate(v) {
    try {
      return new Date(v).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
    } catch (e) { return '—'; }
  }

  function relTime(v) {
    var ms = Date.now() - new Date(v).getTime();
    if (isNaN(ms) || ms < 0) return '—';
    var m = Math.floor(ms / 60000);
    if (m < 1) return 'just now';
    if (m < 60) return m + 'm ago';
    var h = Math.floor(m / 60);
    if (h < 48) return h + 'h ago';
    return Math.floor(h / 24) + 'd ago';
  }

  function freshClass(v) {
    var ms = Date.now() - new Date(v).getTime();
    if (isNaN(ms) || ms < 0) return 'ov-old';
    var h = ms / 3600000;
    if (h < FRESH_H) return 'ov-fresh';
    if (h < STALE_H) return 'ov-stale';
    return 'ov-old';
  }

  function deskName(id) {
    return DESK_NAMES[id] || String(id).replace(/[_-]/g, ' ').toLowerCase()
      .replace(/^./, function (c) { return c.toUpperCase(); });
  }

  function deskMethod(id, registry) {
    if (DESK_METHODS[id]) return DESK_METHODS[id];
    var reg = (registry || []).filter(function (r) { return r && r.project_id === id; })[0];
    if (reg && reg.objective) return String(reg.objective).split('.')[0] + '.';
    return 'Research workflow under evaluation.';
  }

  function deskStatus(p) {
    var s = String(p.data_status || '').toLowerCase();
    return STATUS_WORD[s] ? { word: STATUS_WORD[s], cls: 'ov-' + s } : { word: 'No data', cls: 'ov-none' };
  }

  function brandLockup() {
    return '' +
      '<section class="ov-brand" aria-label="Emporion">' +
        '<svg class="compass" viewBox="0 0 200 200" aria-hidden="true">' +
          '<circle cx="100" cy="100" r="82" fill="none" stroke="currentColor" stroke-width="1"/>' +
          '<path d="M100 10 L112 88 L190 100 L112 112 L100 190 L88 112 L10 100 L88 88 Z" fill="none" stroke="currentColor" stroke-width="1"/>' +
          '<circle cx="100" cy="100" r="10" fill="none" stroke="currentColor" stroke-width="1"/>' +
        '</svg>' +
        '<img class="seal" src="./emporion-institutional-seal.svg" alt="" width="148" height="148">' +
        '<h1>EMPORION</h1>' +
        '<div class="rule" aria-hidden="true"></div>' +
        '<div class="tagline">MARKETS · INTELLIGENCE · DISCIPLINE</div>' +
        '<p class="lede">Six desks. One decision.</p>' +
        '<p class="lede-sub">Live research, evaluated around the clock.</p>' +
      '</section>';
  }

  function hero(data, report, brief) {
    var s = data.summary || {};
    var live = (report.projects || []).filter(function (p) { return p.data_status === 'live'; }).length;
    var total = s.desks_total || (report.projects || []).length || 6;
    var cands = ((data.candidate_feed || {}).candidates || []).length;
    var asOf = s.data_as_of;
    var briefFoot = brief && brief.headline
      ? '<div class="ov-foot">' + esc(String(brief.headline).slice(0, 72)) + '</div>'
      : '<div class="ov-foot ov-muted">Not published yet</div>';
    return '' +
      '<section class="ov-hero" aria-label="Live desk status">' +
        '<h1 class="ov-sr">Hedge Desk — research overview</h1>' +
        '<div class="ov-eyebrow">Hedge desk · Live</div>' +
        '<div class="ov-stats">' +
          '<article class="ov-stat">' +
            '<div class="ov-eyebrow">Desks live</div>' +
            '<div class="ov-value">' + esc(live) + '<small>/' + esc(total) + '</small></div>' +
            '<div class="ov-foot"><i class="ov-dot ' + (live ? 'ov-fresh' : 'ov-old') + '"></i>live market data</div>' +
          '</article>' +
          '<article class="ov-stat">' +
            '<div class="ov-eyebrow">Data as of</div>' +
            '<div class="ov-value ov-value-sm">' + esc(fmtDate(asOf)) + '</div>' +
            '<div class="ov-foot"><i class="ov-dot ' + freshClass(asOf) + '"></i>Yahoo Finance · ' + esc(relTime(asOf)) + '</div>' +
          '</article>' +
          '<article class="ov-stat">' +
            '<div class="ov-eyebrow">Candidates</div>' +
            '<div class="ov-value">' + esc(cands) + '</div>' +
            '<div class="ov-foot">symbols in feed</div>' +
          '</article>' +
          '<article class="ov-stat">' +
            '<div class="ov-eyebrow">Daily brief</div>' +
            '<div class="ov-value ov-value-sm">' + esc(brief && brief.date ? brief.date : '—') + '</div>' +
            briefFoot +
          '</article>' +
        '</div>' +
      '</section>';
  }

  function desks(data, report) {
    var projects = report.projects || [];
    var cards = projects.map(function (p, i) {
      var st = deskStatus(p);
      return '' +
        '<article class="ov-desk">' +
          '<div class="ov-desk-top"><span class="ov-eyebrow">Desk ' + ('0' + (i + 1)).slice(-2) + '</span>' +
          '<span class="ov-status ' + st.cls + '"><i class="ov-dot"></i>' + esc(st.word) + '</span></div>' +
          '<h3>' + esc(deskName(p.project_id)) + '</h3>' +
          '<p>' + esc(deskMethod(p.project_id, data.registry)) + '</p>' +
          '<div class="ov-desk-foot"><span class="mono">as of ' + esc(fmtDate(p.data_as_of)) + '</span></div>' +
        '</article>';
    }).join('');
    return '' +
      '<section class="ov-desks" aria-label="Research desks">' +
        '<div class="ov-eyebrow">Research desks</div>' +
        '<div class="ov-grid">' + cards + '</div>' +
      '</section>';
  }

  function pipeline() {
    var steps = ['Candidate intake', 'Research desks', 'Scenario analysis', 'Risk gate', 'Human review'];
    var items = steps.map(function (label, i) {
      return '<li><span class="ov-step-n">' + ('0' + (i + 1)).slice(-2) + '</span>' +
        '<span class="ov-step-label">' + esc(label) + '</span></li>';
    }).join('');
    return '' +
      '<section class="ov-pipeline" aria-label="Research pipeline">' +
        '<div class="ov-eyebrow">Pipeline</div>' +
        '<ol class="ov-steps">' + items + '</ol>' +
      '</section>';
  }

  function boundary() {
    return '' +
      '<section class="ov-boundary" aria-label="Operating boundary">' +
        '<div class="ov-eyebrow">Boundary</div>' +
        '<p>Paper research only. No orders placed. No real trades.</p>' +
        '<p>Not investment advice. You own your decisions.</p>' +
        '<p>Risk of Ruin is an independent gate — research conviction never overrides it.</p>' +
      '</section>';
  }

  function render(data, report, brief) {
    data = data || {};
    report = report || {};
    return '<div class="ov">' + brandLockup() + hero(data, report, brief) + desks(data, report) + pipeline() + boundary() + '</div>';
  }

  root.HedgeDeskOverview = { render: render };
})(typeof globalThis !== 'undefined' ? globalThis : this);
