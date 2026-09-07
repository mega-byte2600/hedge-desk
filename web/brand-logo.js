const LOGO = './emporion-mark.svg';

function installBrandStyle() {
  if (document.getElementById('emporion-logo-style')) return;
  const style = document.createElement('style');
  style.id = 'emporion-logo-style';
  style.textContent = `
    .brand-logo{width:42px;height:42px;display:block;flex:0 0 42px;border-radius:9px;box-shadow:0 1px 0 rgba(255,255,255,.08)}
    .brand>span{min-width:0}
    .emporion-about-lockup{display:flex;align-items:center;gap:14px;margin-bottom:12px}
    .emporion-about-logo{width:52px;height:52px;display:block;flex:0 0 52px}
    @media(max-width:950px){.brand-logo{width:36px;height:36px;flex-basis:36px}.brand{gap:10px}}
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
    brand.innerHTML = `<img class="brand-logo" src="${LOGO}" alt="" width="42" height="42"><span>EMPORION<small>MARKETS · INTELLIGENCE · DISCIPLINE</small></span>`;
  }

  const aboutHead = document.querySelector('.ws-capital-head > div');
  if (aboutHead && !aboutHead.querySelector('.emporion-about-lockup')) {
    const title = aboutHead.querySelector('h2');
    const brandline = aboutHead.querySelector('.ws-brandline');
    if (title) {
      const lockup = document.createElement('div');
      lockup.className = 'emporion-about-lockup';
      lockup.innerHTML = `<img class="emporion-about-logo" src="${LOGO}" alt="Emporion logo" width="52" height="52"><div><strong>EMPORION</strong><div class="ws-label">MARKETS · INTELLIGENCE · DISCIPLINE</div></div>`;
      title.insertAdjacentElement('beforebegin', lockup);
      title.style.display = 'none';
      if (brandline) brandline.textContent = 'A Bolton Investment Group (BIG) Project';
    }
  }
}

window.addEventListener('DOMContentLoaded', applyLogo);
window.addEventListener('hashchange', () => requestAnimationFrame(applyLogo));

const observer = new MutationObserver(() => requestAnimationFrame(applyLogo));
observer.observe(document.documentElement, {childList:true, subtree:true});
applyLogo();
