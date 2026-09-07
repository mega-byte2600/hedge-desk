function installDeskArchitecture() {
  if (location.hash !== '#desks') return;
  const main = document.getElementById('main');
  const cards = main?.querySelector('.cards');
  if (!cards || cards.querySelector('[data-desk-architecture="bonds-rates-desk"]')) return;

  const panel = document.createElement('article');
  panel.className = 'panel desk-card';
  panel.dataset.deskArchitecture = 'bonds-rates-desk';
  panel.innerHTML = `
    <div style="display:flex;justify-content:space-between;gap:12px;align-items:center">
      <span class="eyebrow">DESK 07 · MACRO ANCHOR</span>
      <span class="tag">Architecture only</span>
    </div>
    <h2>Bonds &amp; Rates</h2>
    <p>Anchor cross-asset research in Treasury curves, real rates, Fed policy, credit spreads, duration, and liquidity stress.</p>
    <div class="gate-bars" aria-label="Architecture defined; evaluated research not yet connected"><span class="gray"></span><span class="gray"></span><span class="gray"></span><span class="gray"></span><span class="gray"></span><span class="gray"></span></div>
    <a class="btn" href="#resources">View institutional rates sources ↗</a>
    <p class="small-note">No evaluated signal is published for this desk yet.</p>`;
  cards.prepend(panel);

  const head = main.querySelector('.page-head .subtitle');
  if (head) head.textContent = 'Seven-desk architecture. Six workflows are currently evaluated; Bonds & Rates is the next anchor desk.';
}

window.addEventListener('hashchange', () => requestAnimationFrame(installDeskArchitecture));
window.addEventListener('DOMContentLoaded', () => {
  const main = document.getElementById('main');
  if (main) new MutationObserver(() => requestAnimationFrame(installDeskArchitecture)).observe(main, {childList:true, subtree:false});
  requestAnimationFrame(installDeskArchitecture);
});
