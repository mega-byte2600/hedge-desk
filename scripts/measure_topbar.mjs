// Measures the topbar gap on the live page. Evidence, not opinion:
// the defect was the status text sitting flush against the breadcrumb.
import { launchEngine } from './playwright_loader.mjs';

const url = (process.argv[2] || 'http://127.0.0.1:8765') + '/#about';
const launched = await launchEngine('chromium');
if (launched.error) { console.log('SKIP: no browser available - ' + launched.error); process.exit(0); }
const { browser } = launched;
const page = await browser.newPage();
const width = Number(process.argv[3] || 1440);
await page.setViewportSize({ width, height: 900 });
await page.goto(url, { waitUntil: 'load' });
await page.waitForTimeout(1200);

const m = await page.evaluate(() => {
  const bar = document.querySelector('.topbar');
  const bc = document.querySelector('#breadcrumb');
  const st = document.querySelector('.top-status');
  const acct = document.querySelector('.top-account');
  const r = (el) => { const b = el.getBoundingClientRect(); return { left: +b.left.toFixed(1), right: +b.right.toFixed(1) }; };
  return {
    breadcrumbText: bc ? bc.textContent.trim() : null,
    statusText: st ? st.textContent.trim() : null,
    statusDisplay: st ? getComputedStyle(st).display : null,
    statusMarginLeft: st ? getComputedStyle(st).marginLeft : null,
    breadcrumb: bc ? r(bc) : null,
    status: st ? r(st) : null,
    acct: acct ? r(acct) : null,
    barRight: bar ? +bar.getBoundingClientRect().right.toFixed(1) : null,
    overflowX: document.documentElement.scrollWidth > window.innerWidth,
  };
});

const gap = (m.status && m.breadcrumb) ? +(m.status.left - m.breadcrumb.right).toFixed(1) : null;
const acctGap = (m.acct && m.status) ? +(m.acct.left - m.status.right).toFixed(1) : null;

console.log(JSON.stringify({
  url,
  breadcrumb: m.breadcrumbText,
  status: m.statusText,
  statusDisplay: m.statusDisplay,
  statusMarginLeft: m.statusMarginLeft,
  GAP_breadcrumb_to_status_px: gap,
  GAP_status_to_account_px: acctGap,
  overflowX: m.overflowX,
}, null, 2));
await browser.close();
