function route() {
  return (location.hash || '#overview').slice(1).split('?')[0] || 'overview';
}

const subtitles = {
  overview: 'Six research workflows, operating state, and decision controls.',
  candidates: 'Research universe by desk, method, and required evidence.',
  desks: 'Methods, evidence requirements, and control state for each research workflow.',
  scenarios: 'Deterministic scenario coverage and portfolio stress testing.',
  controls: 'Data provenance, release requirements, and control boundaries.',
  journal: 'Why enter. What would prove the thesis wrong. Why exit. What did we learn.',
  about: 'Emporion research platform, governance, and project background.'
};

function polishCopy() {
  const current = route();
  const subtitle = document.querySelector('#main .page-head .subtitle');
  if (subtitle && subtitles[current]) subtitle.textContent = subtitles[current];

  if (current === 'about') {
    const about = document.querySelector('.about-card');
    if (about) {
      const eyebrow = about.querySelector('.eyebrow');
      if (eyebrow) eyebrow.textContent = 'FOUNDER / BUILDER';
      const paragraphs = about.querySelectorAll('p');
      if (paragraphs[0]) paragraphs[0].textContent = 'Emporion is an independent, paper-only market research and decision platform built around six specialized research workflows, explicit evidence requirements, deterministic controls, and human judgment.';
      if (paragraphs[1]) paragraphs[1].textContent = 'Research automation remains separate from deterministic portfolio-survival controls. Live trading and fully autonomous execution are outside the current MVP.';
    }
  }

  document.querySelectorAll('#main .subtitle').forEach(node => {
    node.textContent = node.textContent
      .replace('Your desk, before the next decision.', subtitles.overview)
      .replace('Inspect each workflow, its evidence, and what stops the next decision.', subtitles.desks)
      .replace('The builder behind Trade Desk Research.', subtitles.about);
  });
}

window.addEventListener('hashchange', () => requestAnimationFrame(polishCopy));
window.addEventListener('DOMContentLoaded', () => {
  const main = document.querySelector('main');
  if (main) {
    new MutationObserver(() => requestAnimationFrame(polishCopy)).observe(main, {childList:true, subtree:true});
  }
  polishCopy();
});
