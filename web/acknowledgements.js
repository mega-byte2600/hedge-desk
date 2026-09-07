function currentRoute() {
  return (location.hash || '#overview').slice(1).split('?')[0] || 'overview';
}

function acknowledgementBlock() {
  const route = currentRoute();
  if (!['journal', 'about'].includes(route)) return;
  const main = document.querySelector('#main');
  const head = main?.querySelector('.page-head');
  if (!main || !head || document.querySelector('#campbell-acknowledgement')) return;

  const section = document.createElement('section');
  section.id = 'campbell-acknowledgement';
  section.className = 'panel campbell-ack';
  section.setAttribute('aria-label', 'Special acknowledgement');
  section.innerHTML = `
    <div class="panel-head">
      <div>
        <div class="eyebrow">SPECIAL ACKNOWLEDGEMENT</div>
        <h2>William Campbell, Ph.D.</h2>
        <p>University of Wyoming MBA Program</p>
      </div>
    </div>
    <div class="panel-body">
      <p>Emporion gratefully acknowledges Dr. Campbell for sharing professional trade-desk perspective and feedback that helped shape the discipline behind the Yellow Sheet and Trade Log: document why a position is entered, define the plan before capital is committed, record why it is exited, and review what was learned.</p>
      <p class="small">Acknowledgement reflects educational mentorship and feedback. It does not imply endorsement, sponsorship, investment advice, or responsibility for Emporion's models, controls, research outputs, or investment results.</p>
    </div>`;

  if (route === 'journal') {
    const loop = document.querySelector('#yellow-sheet-feedback-loop');
    (loop || head).insertAdjacentElement('afterend', section);
  } else {
    const capital = document.querySelector('.ws-capital');
    (capital || head).insertAdjacentElement('afterend', section);
  }
}

function installStyle() {
  if (document.getElementById('campbell-ack-style')) return;
  const style = document.createElement('style');
  style.id = 'campbell-ack-style';
  style.textContent = `
    .campbell-ack{margin:0 0 27px;border-left:3px solid #101820}
    .campbell-ack .panel-head{background:#fafbfc}
    .campbell-ack .panel-head h2{margin-top:7px}
    .campbell-ack .panel-head p{margin-top:5px}
    .campbell-ack .panel-body>p:first-child{max-width:940px;line-height:1.65}
  `;
  document.head.appendChild(style);
}

function renderAcknowledgement() {
  installStyle();
  document.querySelector('#campbell-acknowledgement')?.remove();
  acknowledgementBlock();
}

window.addEventListener('hashchange', () => requestAnimationFrame(renderAcknowledgement));
window.addEventListener('DOMContentLoaded', () => {
  const main = document.querySelector('main');
  if (main) {
    const observer = new MutationObserver(() => {
      if (!document.querySelector('#campbell-acknowledgement')) requestAnimationFrame(renderAcknowledgement);
    });
    observer.observe(main, {childList:true, subtree:true});
  }
  renderAcknowledgement();
});
