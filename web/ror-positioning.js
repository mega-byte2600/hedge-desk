function applyRoRPositioning() {
  const riskBlock = document.querySelector('.ws-ror');
  if (riskBlock && riskBlock.dataset.positioned !== 'true') {
    riskBlock.dataset.positioned = 'true';
    riskBlock.setAttribute('aria-label', 'Emporion North Star: portfolio survival');
    riskBlock.innerHTML = `
      <div class="ws-label">NORTH STAR · RISK OF RUIN</div>
      <div class="ws-ror-grid">
        <article><h2>Survive first. Compound second.</h2><p>Emporion treats Risk of Ruin as an independent constraint on every decision, not an afterthought to conviction.</p></article>
        <article><h3>Point of difference</h3><p>Research can build conviction. It cannot override portfolio survival.</p></article>
        <article><h3>Credit</h3><p>Dr. Cooper helped bring the explicit Risk of Ruin discipline to the table.</p></article>
      </div>`;
  }

  const riskTape = [...document.querySelectorAll('.ws-tape span')].find(node => node.textContent?.trim().startsWith('RISK'));
  if (riskTape) riskTape.innerHTML = '<b>RISK</b> SURVIVAL FIRST';
}

const observer = new MutationObserver(() => applyRoRPositioning());
window.addEventListener('DOMContentLoaded', () => {
  applyRoRPositioning();
  const main = document.querySelector('main');
  if (main) observer.observe(main, { childList: true, subtree: true });
});
window.addEventListener('hashchange', () => requestAnimationFrame(applyRoRPositioning));
