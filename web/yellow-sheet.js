import { escapeHTML as e, human, readNotes } from './core.mjs';

const KEY = 'trade-desk-yellow-sheets-v1';
const main = document.querySelector('#main');

function renameLabel(control, text) {
  const label = control?.closest('label');
  if (!label) return;
  const node = [...label.childNodes].find(n => n.nodeType === Node.TEXT_NODE);
  if (node && node.textContent !== text) node.textContent = text;
}

function addField(before, html) {
  if (before) before.insertAdjacentHTML('beforebegin', html);
}

function setText(node, value) {
  if (node && node.textContent !== value) node.textContent = value;
}

function enhanceForm() {
  const form = document.querySelector('#note-form');
  if (!form || form.dataset.yellowSheetEnhanced === 'true') return;
  form.dataset.yellowSheetEnhanced = 'true';

  const thesis = form.querySelector('[name="thesis"]');
  const evidence = form.querySelector('[name="evidence"]');
  const invalidation = form.querySelector('[name="invalidation"]');

  renameLabel(thesis, 'Why Enter / Investment Thesis');
  renameLabel(evidence, 'Evidence / Catalyst');
  renameLabel(invalidation, 'What Would Prove Me Wrong?');
  if (thesis.placeholder !== 'Why does this position deserve capital now?') thesis.placeholder = 'Why does this position deserve capital now?';
  if (evidence.placeholder !== 'What point in time evidence and catalysts support the thesis?') evidence.placeholder = 'What point in time evidence and catalysts support the thesis?';
  if (invalidation.placeholder !== 'What fact, price action, event, or management change invalidates the thesis?') invalidation.placeholder = 'What fact, price action, event, or management change invalidates the thesis?';

  addField(thesis?.closest('label'), `
    <div class="ys-inline-grid">
      <label class="form-field">Symbol / Contract<input class="input" name="symbol" maxlength="40" placeholder="e.g., SPY or ES"></label>
      <label class="form-field">Position / Instrument<input class="input" name="position" maxlength="120" placeholder="e.g., defined risk put spread"></label>
      <label class="form-field">Investment Horizon<input class="input" name="horizon" maxlength="80" placeholder="e.g., 1 to 12 weeks"></label>
    </div>`);

  invalidation?.closest('label')?.insertAdjacentHTML('afterend', `
    <label class="form-field">Planned Exit / Roll Rule<textarea class="input" name="planned_exit" maxlength="3000" placeholder="Define target, stop, time based exit, roll rule, or event trigger before entry."></textarea></label>
    <details class="ys-closeout">
      <summary>Trade Log Closeout <span>complete when the paper position closes</span></summary>
      <div class="ys-closeout-body">
        <div class="ys-inline-grid">
          <label class="form-field">Lifecycle Status<select class="input" name="trade_status"><option value="RESEARCH">Research</option><option value="NO_TRADE">No Trade</option><option value="PAPER_OPEN">Paper Open</option><option value="PAPER_CLOSED">Paper Closed</option></select></label>
          <label class="form-field">Entry Execution / Price<input class="input" name="entry_execution" maxlength="80" placeholder="optional"></label>
          <label class="form-field">Exit Execution / Price<input class="input" name="exit_execution" maxlength="80" placeholder="optional"></label>
        </div>
        <label class="form-field">Why Exit<textarea class="input" name="why_exit" maxlength="3000" placeholder="Why did the position close? Cite the original plan, invalidation, risk action, or changed thesis."></textarea></label>
        <label class="form-field">Post Trade Review<textarea class="input" name="post_trade_review" maxlength="3000" placeholder="What was learned? What, if anything, should change in future research or controls?"></textarea></label>
      </div>
    </details>`);

  const submit = form.querySelector('button[type="submit"]');
  setText(submit, 'Save Yellow Sheet');
  const note = submit?.nextElementSibling;
  setText(note, 'Bound to the displayed report hash. The Yellow Sheet records judgment; it never overrides deterministic risk or compliance controls.');
}

function lifecyclePanel() {
  if (document.querySelector('#yellow-sheet-feedback-loop')) return;
  const head = document.querySelector('#main .page-head');
  if (!head) return;
  head.insertAdjacentHTML('afterend', `
    <section id="yellow-sheet-feedback-loop" class="panel ys-feedback" aria-labelledby="ys-loop-title">
      <div class="panel-head"><div><div class="eyebrow">DECISION FEEDBACK LOOP</div><h2 id="ys-loop-title">One thesis. Full trade lifecycle.</h2><p>Every position starts with a reason, passes independent controls, and closes with an explicit explanation of what changed.</p></div></div>
      <div class="ys-flow" aria-label="Candidate to research feedback lifecycle">
        <div class="ys-step"><b>1</b><strong>Candidate</strong><span>Research idea</span></div><i>→</i>
        <div class="ys-step focus"><b>2</b><strong>Why Enter</strong><span>Yellow Sheet</span></div><i>→</i>
        <div class="ys-step"><b>3</b><strong>Risk + Compliance</strong><span>Independent gates</span></div><i>→</i>
        <div class="ys-step"><b>4</b><strong>Human Decision</strong><span>Exact plan</span></div><i>→</i>
        <div class="ys-step"><b>5</b><strong>Trade Log</strong><span>Paper lifecycle</span></div><i>→</i>
        <div class="ys-step focus"><b>6</b><strong>Why Exit</strong><span>Yellow Sheet closeout</span></div><i>→</i>
        <div class="ys-step"><b>7</b><strong>Post Trade Review</strong><span>Outcome + lesson</span></div><i class="ys-return">↺</i>
        <div class="ys-step"><b>8</b><strong>Research Feedback</strong><span>Improve the next decision</span></div>
      </div>
      <div class="ys-principle"><strong>Control principle</strong><span>The Yellow Sheet explains the human thesis and its evolution. Deterministic risk and compliance remain separate, binding, and non overridable.</span></div>
    </section>`);
}

function enhanceHeadings() {
  const heading = document.querySelector('#main .page-head h1');
  const subtitle = document.querySelector('#main .page-head .subtitle');
  setText(heading, 'Yellow Sheets + Trade Log');
  setText(subtitle, 'Why enter. What would prove the thesis wrong. Why exit. What did we learn.');

  const panels = document.querySelectorAll('#main .journal-layout > .panel');
  const firstTitle = panels[0]?.querySelector('.panel-head h2');
  const firstSub = panels[0]?.querySelector('.panel-head p');
  const secondTitle = panels[1]?.querySelector('.panel-head h2');
  const secondSub = panels[1]?.querySelector('.panel-head p');
  setText(firstTitle, 'New Yellow Sheet');
  setText(firstSub, 'Pre trade thesis first. Closeout when the paper position exits.');
  setText(secondTitle, 'Trade Log / Yellow Sheet History');
  if (secondSub) setText(secondSub, secondSub.textContent.replace('saved notes', 'lifecycle records').replace('saved note', 'lifecycle record'));
}

function enhanceSavedNotes() {
  let notes;
  try { notes = readNotes(localStorage).slice().reverse(); } catch { return; }
  const cards = [...document.querySelectorAll('#main .journal-layout .saved-note')];
  cards.forEach((card, index) => {
    if (card.querySelector('.ys-record')) return;
    const n = notes[index];
    if (!n) return;
    const eyebrow = card.querySelector('.eyebrow');
    if (n.symbol && eyebrow) eyebrow.textContent = `${n.symbol} · ${eyebrow.textContent}`;
    const status = human(n.trade_status || 'RESEARCH');
    const block = document.createElement('div');
    block.className = 'ys-record';
    block.innerHTML = `
      <div class="ys-record-meta"><span>${e(status)}</span>${n.position ? `<span>${e(n.position)}</span>` : ''}${n.horizon ? `<span>${e(n.horizon)}</span>` : ''}</div>
      ${n.planned_exit ? `<p><strong>Planned Exit / Roll Rule</strong><br>${e(n.planned_exit)}</p>` : ''}
      ${n.entry_execution || n.exit_execution ? `<p><strong>Trade Log</strong><br>Entry: ${e(n.entry_execution || 'not recorded')} · Exit: ${e(n.exit_execution || 'not recorded')}</p>` : ''}
      ${n.why_exit ? `<p><strong>Why Exit</strong><br>${e(n.why_exit)}</p>` : ''}
      ${n.post_trade_review ? `<p><strong>Post Trade Review</strong><br>${e(n.post_trade_review)}</p>` : ''}`;
    card.appendChild(block);
  });
}

function enhance() {
  if (location.hash !== '#journal') return;
  lifecyclePanel();
  enhanceHeadings();
  enhanceForm();
  enhanceSavedNotes();
}

const observer = new MutationObserver(() => queueMicrotask(enhance));
if (main) observer.observe(main, { childList: true, subtree: true });
window.addEventListener('hashchange', () => queueMicrotask(enhance));
queueMicrotask(enhance);

// app.js saves the base research record; extend that same record with the
// lifecycle fields without touching the engine or authorization boundary.
//
// Ordering matters and is easy to get wrong. app.js registers its `document`
// submit listener first (index.html loads app.js before this module) and saves the
// record synchronously inside that listener, so by the time this listener runs the
// note is already stored — this listener is deliberately a bubble-phase listener
// with no deferral, and it extends the last stored record directly.
//
// Two variants that look right and are not:
//   * deferring with queueMicrotask: a microtask queued in a submit listener drains
//     at the checkpoint right after that listener returns, i.e. *before* app.js's
//     bubble listener saves, so the record being extended does not exist yet;
//   * relying on a note-count delta: this listener reads the count after the base
//     save, so an "expect exactly one more" guard can never be satisfied.
document.addEventListener('submit', event => {
  if (event.target?.id !== 'note-form') return;
  const form = event.target;
  const values = Object.fromEntries(new FormData(form).entries());
  try {
    const notes = readNotes(localStorage);
    const last = notes[notes.length - 1];
    // The base save must have landed for this submission, and this must be the
    // first extension of it (the listener is idempotent).
    if (!last || last.thesis !== values.thesis || last.yellow_sheet_extended) return;
    Object.assign(last, {
        symbol: String(values.symbol || '').trim().toUpperCase(),
        position: String(values.position || '').trim(),
        horizon: String(values.horizon || '').trim(),
        planned_exit: String(values.planned_exit || '').trim(),
        trade_status: String(values.trade_status || 'RESEARCH'),
        entry_execution: String(values.entry_execution || '').trim(),
        exit_execution: String(values.exit_execution || '').trim(),
        why_exit: String(values.why_exit || '').trim(),
        post_trade_review: String(values.post_trade_review || '').trim(),
        yellow_sheet_extended: true
    });
    localStorage.setItem(KEY, JSON.stringify(notes));
    enhanceSavedNotes();
  } catch {
    // Base journal behavior remains authoritative if browser storage is invalid.
  }
});
