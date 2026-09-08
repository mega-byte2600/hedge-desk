(() => {
  const main = document.querySelector('#main');
  if (!main) return;

  const markup = `
    <section class="panel" data-candidate-context>
      <div class="panel-head">
        <div>
          <div class="eyebrow">HOW EMPORION TURNS A SYMBOL INTO A DECISION</div>
          <h2>Candidates are the research queue, not recommendations.</h2>
          <p>Emporion brings an institutional-style trade decision workflow into one open research workspace: Research the idea. Challenge the thesis. Document the reasoning. Decide with discipline.</p>
        </div>
      </div>
      <div class="panel-body">
        <div class="notice"><strong>COORDINATED RESEARCH SYSTEM</strong><span>Seven research desks. Specialized research agents in each. One coordinated decision process.</span></div>
        <p>Each desk is designed to be supported by one or more specialized research agents working as research analysts for that domain. Across Emporion, those agents can collaborate across desks, share findings, challenge assumptions, and synthesize intelligence into a coordinated research process.</p>
        <div class="pipeline-line"><span><strong>1 · Candidate intake</strong><br><small>A symbol enters the research universe.</small></span><strong>START</strong></div>
        <div class="pipeline-line"><span><strong>2 · Desk research</strong><br><small>Specialized desk agents investigate the idea using the research method and evidence relevant to that desk.</small></span><strong>RESEARCH</strong></div>
        <div class="pipeline-line"><span><strong>3 · Evidence qualification</strong><br><small>Required market evidence must be present before a candidate can become method-qualified.</small></span><strong>QUALIFY</strong></div>
        <div class="pipeline-line"><span><strong>4 · Scenario + Yellow Sheet</strong><br><small>The thesis is challenged under scenarios and the reasoning is documented before a decision.</small></span><strong>CHALLENGE</strong></div>
        <div class="pipeline-line"><span><strong>5 · Human decision</strong><br><small>Research supports judgment. Emporion does not authorize a trade.</small></span><strong>DECIDE</strong></div>
        <p class="small">This MVP demonstrates that decision process using the Published paper snapshot. Current market evidence and method scoring remain explicitly disconnected on this page. Emporion supports a path toward user-controlled automated trading through future data, model, broker, and execution integrations, but automated trading is not part of the current MVP.</p>
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