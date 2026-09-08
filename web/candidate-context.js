(() => {
  const main = document.querySelector('#main');
  if (!main) return;

  const markup = `
    <section class="panel" data-candidate-context>
      <div class="panel-head">
        <div>
          <div class="eyebrow">HOW EMPORION TURNS A SYMBOL INTO A DECISION</div>
          <h2>Candidates are the research queue, not recommendations.</h2>
          <p>Emporion brings an institutional-style trade decision workflow into one open research workspace: research the idea, challenge the thesis, document the reasoning, and decide with discipline.</p>
        </div>
      </div>
      <div class="panel-body">
        <div class="notice"><strong>INSTITUTIONAL-STYLE TRADE DECISION WORKFLOW</strong><span>Research the idea → Challenge the thesis → Decide with discipline.</span></div>
        <div class="pipeline-line"><span><strong>1 · Candidate intake</strong><br><small>A symbol enters the research universe.</small></span><strong>START</strong></div>
        <div class="pipeline-line"><span><strong>2 · Desk method</strong><br><small>The idea is assigned to one of the six evaluated research workflows.</small></span><strong>RESEARCH</strong></div>
        <div class="pipeline-line"><span><strong>3 · Evidence qualification</strong><br><small>Required market evidence must be present before a candidate can become method-qualified.</small></span><strong>QUALIFY</strong></div>
        <div class="pipeline-line"><span><strong>4 · Scenario + Yellow Sheet</strong><br><small>The thesis is challenged under scenarios and the reasoning is documented before a decision.</small></span><strong>CHALLENGE</strong></div>
        <div class="pipeline-line"><span><strong>5 · Human decision</strong><br><small>Research supports judgment. Emporion does not authorize a trade.</small></span><strong>DECIDE</strong></div>
        <p class="small">This MVP demonstrates that decision process using the Published paper snapshot. Current market evidence and method scoring remain explicitly disconnected on this page. The open architecture can be extended by users into their own data, model, and execution workflows; those integrations are not shipped as live trading functionality in this build.</p>
      </div>
    </section>`;

  function enhanceCandidates() {
    if ((location.hash.slice(1) || 'candidates') !== 'candidates') return;
    if (main.querySelector('[data-candidate-context]')) return;
    const stats = main.querySelector('.stats');
    if (!stats) return;
    stats.insertAdjacentHTML('beforebegin', markup);
  }

  const observer = new MutationObserver(enhanceCandidates);
  observer.observe(main, { childList: true, subtree: true });
  window.addEventListener('hashchange', enhanceCandidates);
  enhanceCandidates();
})();