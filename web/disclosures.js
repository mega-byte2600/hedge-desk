// Renders the versioned disclosures on the About tab.
//
// Follows the conventions the rest of the console settled on after two freeze bugs:
// the enhancement is guarded (idempotent) and its observer callback is deferred with
// requestAnimationFrame, so it can never re-enter itself and lock the main thread.
import { currentRoute } from './core.mjs';

const MOUNT_ID = 'emporion-disclosures';

async function loadDisclosures() {
  const response = await fetch('./disclosures.json', { cache: 'no-store' });
  if (!response.ok) throw new Error('disclosures unavailable');
  const payload = await response.json();
  if (payload?.schema_version !== 'emporion-disclosures-1' || !Array.isArray(payload.disclosures)) {
    throw new Error('unsupported disclosures payload');
  }
  return payload;
}

function disclosureMarkup(payload) {
  const items = payload.disclosures
    .map((d) => `<article class="disclosure-item" style="padding:14px 0;border-top:1px solid #e1e6e9">
        <h3 style="margin:0 0 6px;font-size:13px">${escapeText(d.title)}</h3>
        <p style="margin:0;font-size:12px;line-height:1.6;color:#596871">${escapeText(d.text)}</p>
      </article>`)
    .join('');
  return `<section id="${MOUNT_ID}" class="panel" style="margin-top:18px" aria-labelledby="disclosures-title">
      <div class="panel-head"><div>
        <div class="eyebrow">DISCLOSURES · VERSION ${escapeText(payload.disclosure_version)}</div>
        <h2 id="disclosures-title">What this desk is and is not</h2>
        <p>Effective ${escapeText(payload.effective)}. Stated plainly, because a research tool that
        hides its boundaries is not usable for real decisions.</p>
      </div></div>
      <div class="panel-body">${items}</div>
    </section>`;
}

function escapeText(value) {
  return String(value ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

async function renderDisclosures() {
  if (document.getElementById(MOUNT_ID)) return;      // idempotent
  if (currentRoute() !== 'about') return;
  const main = document.querySelector('#main');
  if (!main) return;
  const host = main.querySelector('.about-card')?.closest('.panel') || main.querySelector('.panel');
  if (!host) return;
  try {
    const payload = await loadDisclosures();
    if (document.getElementById(MOUNT_ID)) return;    // re-check after await
    host.insertAdjacentHTML('afterend', disclosureMarkup(payload));
  } catch {
    // The About tab remains fully usable without the disclosures block; do not
    // fabricate content, and do not break the page over a static asset.
  }
}

window.addEventListener('hashchange', () => requestAnimationFrame(renderDisclosures));
window.addEventListener('DOMContentLoaded', () => {
  const main = document.querySelector('#main');
  if (main) {
    new MutationObserver(() => requestAnimationFrame(renderDisclosures)).observe(main, { childList: true, subtree: true });
  }
  requestAnimationFrame(renderDisclosures);
});
