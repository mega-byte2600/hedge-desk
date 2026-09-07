function currentRoute() {
  return (location.hash || '#overview').slice(1).split('?')[0] || 'overview';
}

function acknowledgementBlock() {
  if (currentRoute() !== 'about') return;
  const inspirations = document.querySelector('.ws-inspiration');
  if (!inspirations || inspirations.querySelector('#campbell-acknowledgement')) return;

  const section = document.createElement('div');
  section.id = 'campbell-acknowledgement';
  section.className = 'campbell-ack';
  section.setAttribute('aria-label', 'Special acknowledgement');
  section.innerHTML = `
    <div class="ws-label">SPECIAL ACKNOWLEDGEMENT</div>
    <p><strong>William Campbell, Ph.D. · University of Wyoming MBA Program</strong></p>
    <p>Emporion gratefully acknowledges Dr. Campbell for professional trade-desk perspective and feedback that helped shape the discipline behind the Yellow Sheet and Trade Log: document why a position is entered, define the plan before capital is committed, record why it is exited, and review what was learned.</p>
    <p class="ws-inspiration-note">Educational mentorship and feedback only. This acknowledgement does not imply endorsement, sponsorship, investment advice, or responsibility for Emporion's research, controls, or results.</p>`;
  inspirations.appendChild(section);

  const contact = document.createElement('div');
  contact.id = 'emporion-contribute-contact';
  contact.className = 'emporion-contact';
  contact.setAttribute('aria-label', 'Contribute and contact');
  contact.innerHTML = `
    <div class="ws-label">CONTRIBUTE / CONTACT</div>
    <p>Emporion is an open-source research project. Researchers, engineers, data practitioners, and other contributors are welcome to review the repository, open an issue, submit a pull request, or get in touch.</p>
    <p class="emporion-contact-links"><a href="https://github.com/mega-byte2600/hedge-desk" target="_blank" rel="noopener noreferrer">GitHub repository ↗</a><span aria-hidden="true">·</span><a href="mailto:michael.bolton.ph@dartmouth.edu">michael.bolton.ph@dartmouth.edu</a></p>`;
  inspirations.appendChild(contact);
}

function installStyle() {
  if (document.getElementById('campbell-ack-style')) return;
  const style = document.createElement('style');
  style.id = 'campbell-ack-style';
  style.textContent = `
    .campbell-ack,.emporion-contact{margin-top:18px;padding-top:18px;border-top:1px solid #e1e6e9}
    .campbell-ack p,.emporion-contact p{max-width:980px}
    .campbell-ack p:last-child,.emporion-contact p:last-child{margin-bottom:0}
    .emporion-contact-links{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
    .emporion-contact a{font-weight:600;text-decoration:none}
    .emporion-contact a:hover{text-decoration:underline}
  `;
  document.head.appendChild(style);
}

function renderAcknowledgement() {
  installStyle();
  document.querySelector('#campbell-acknowledgement')?.remove();
  document.querySelector('#emporion-contribute-contact')?.remove();
  acknowledgementBlock();
}

window.addEventListener('hashchange', () => requestAnimationFrame(renderAcknowledgement));
window.addEventListener('DOMContentLoaded', () => {
  const main = document.querySelector('main');
  if (main) {
    const observer = new MutationObserver(() => {
      if (currentRoute() === 'about' && !document.querySelector('#campbell-acknowledgement')) requestAnimationFrame(renderAcknowledgement);
    });
    observer.observe(main, {childList:true, subtree:true});
  }
  renderAcknowledgement();
});
