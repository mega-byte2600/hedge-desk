function applyRoRPositioning() {
  // The page renders TWO `.ws-ror` blocks: the coordinated-research-architecture
  // section and, below it, the portfolio-survival section. A bare
  // querySelector('.ws-ror') took the first, so this enhancement replaced the
  // architecture copy with a second copy of the survival copy — the architecture
  // block disappeared from the page and the real survival block was left alone.
  // Target the survival block explicitly.
  const riskBlock = [...document.querySelectorAll('.ws-ror')].find(
    (node) => node.dataset.riskOfRuin === 'true' || /RISK OF RUIN/i.test(node.textContent || '')
  );
  if (!riskBlock) return;
  if (riskBlock.dataset.positioned === 'true') return;
  riskBlock.dataset.positioned = 'true';
  riskBlock.setAttribute('aria-label', 'Emporion North Star: portfolio survival');

  // Additive, never a replacement. This block already carries language the short
  // north-star copy below does not — that the reference RoR model is unvalidated
  // and that human review happens only after the risk state is known. Replacing
  // the block's markup deleted that copy, so only the two genuinely new pieces
  // (the north-star label and the credit line) are inserted.
  if (!riskBlock.querySelector('[data-rr-northstar]')) {
    riskBlock.insertAdjacentHTML(
      'afterbegin',
      '<div class="ws-label" data-rr-northstar>NORTH STAR · RISK OF RUIN</div>'
    );
  }
  if (!riskBlock.querySelector('[data-rr-credit]')) {
    riskBlock.insertAdjacentHTML(
      'beforeend',
      '<p data-rr-credit style="margin:0;padding:14px 20px 0;font-size:12px;line-height:1.6;color:#596871">' +
        '<strong>Credit</strong> — Dr. Cooper helped bring the explicit Risk of Ruin discipline to the table.' +
        '</p>'
    );
  }

  // Idempotent on purpose: the MutationObserver below is registered on
  // `main` with subtree:true, so any write here re-enters this function. The
  // risk block is already guarded by its `positioned` flag; the tape needed
  // the same guard. Without it the observer re-fires on its own mutation and
  // the page spin-locks the main thread (the console freezes solid).
  const riskTape = [...document.querySelectorAll('.ws-tape span')].find(node => node.textContent?.trim().startsWith('RISK'));
  if (riskTape && riskTape.dataset.rorTape !== 'true') {
    riskTape.dataset.rorTape = 'true';
    riskTape.innerHTML = '<b>RISK</b> SURVIVAL FIRST';
  }
}

// Deferred like the other page enhancers: a synchronous mutation callback can
// re-enter itself and lock the main thread before the browser ever paints.
const observer = new MutationObserver(() => requestAnimationFrame(applyRoRPositioning));
window.addEventListener('DOMContentLoaded', () => {
  applyRoRPositioning();
  const main = document.querySelector('main');
  if (main) observer.observe(main, { childList: true, subtree: true });
});
window.addEventListener('hashchange', () => requestAnimationFrame(applyRoRPositioning));
