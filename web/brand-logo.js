const LOGO = './emporion-institutional-seal.svg';

function installBrandStyle() {
  if (document.getElementById('emporion-logo-style')) return;
  const style = document.createElement('style');
  style.id = 'emporion-logo-style';
  style.textContent = `
    .brand-logo{width:46px;height:46px;display:block;flex:0 0 46px;border-radius:50%;filter:drop-shadow(0 2px 5px rgba(0,0,0,.28))}
    .brand>span{min-width:0}
    .emporion-about-lockup{display:flex;align-items:center;gap:16px;margin-bottom:12px}
    .emporion-about-logo{width:64px;height:64px;display:block;flex:0 0 64px;border-radius:50%;filter:drop-shadow(0 2px 6px rgba(0,0,0,.18))}
    @media(max-width:950px){.brand-logo{width:40px;height:40px;flex-basis:40px}.brand{gap:10px}}
  `;
  document.head.appendChild(style);
}

function applyLogo() {
  installBrandStyle();
  document.title = 'Emporion | Markets · Intelligence · Discipline';

  const icon = document.querySelector('link[rel="icon"]');
  if (icon) {
    icon.setAttribute('href', LOGO);
    icon.setAttribute('type', 'image/svg+xml');
  }

  const brand = document.querySelector('.brand');
  if (brand && !brand.querySelector('.brand-logo')) {
    brand.setAttribute('aria-label', 'Emporion home');
    brand.innerHTML = `<img class="brand-logo" src="${LOGO}" alt="" width="46" height="46"><span>EMPORION<small>MARKETS · INTELLIGENCE · DISCIPLINE</small></span>`;
  } else if (brand) {
    const img = brand.querySelector('.brand-logo');
    if (img) img.setAttribute('src', LOGO);
  }

  const aboutHead = document.querySelector('.ws-capital-head > div');
  if (aboutHead && !aboutHead.querySelector('.emporion-about-lockup')) {
    const title = aboutHead.querySelector('h2');
    const brandline = aboutHead.querySelector('.ws-brandline');
    if (title) {
      const lockup = document.createElement('div');
      lockup.className = 'emporion-about-lockup';
      lockup.innerHTML = `<img class="emporion-about-logo" src="${LOGO}" alt="Emporion Institutional Seal" width="64" height="64"><div><strong>EMPORION</strong><div class="ws-label">MARKETS · INTELLIGENCE · DISCIPLINE</div></div>`;
      title.insertAdjacentElement('beforebegin', lockup);
      title.style.display = 'none';
      if (brandline) brandline.textContent = 'A Bolton Investment Group (BIG) Project';
    }
  } else if (aboutHead) {
    const img = aboutHead.querySelector('.emporion-about-logo');
    if (img) img.setAttribute('src', LOGO);
  }
}

window.addEventListener('DOMContentLoaded', applyLogo);
window.addEventListener('hashchange', () => requestAnimationFrame(applyLogo));

const observer = new MutationObserver(() => requestAnimationFrame(applyLogo));
observer.observe(document.documentElement, {childList:true, subtree:true});
applyLogo();
