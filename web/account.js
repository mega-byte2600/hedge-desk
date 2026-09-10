/* Membership / auth UI for the Emporion desk.
 *
 * The research console stays open (guest "test drive" tier is public). This
 * adds an opt-in membership layer:
 *   - a Sign in / account control in the topbar,
 *   - an email-OTP sign-in flow (no password),
 *   - role-aware UI (guest / member / LP / GP),
 *   - self-serve subscription (MEMBER) and GP invite (LP) surfaces.
 *
 * Email-OTP auth means every sign-in captures a verified, consent-collected
 * email -> the GP's first-party marketing list.
 */

const ACCT = {
  modal: null,
  current: null, // {authenticated, email, role, access, reason}
  state: 'idle', // idle | sending | verifying
};

function acctEls() {
  return {
    btn: document.getElementById('acct-btn'),
    label: document.getElementById('acct-label'),
  };
}

function acctFetch(path, options = {}) {
  const opts = Object.assign(
    { credentials: 'same-origin', headers: { 'Content-Type': 'application/json' } },
    options,
  );
  return fetch(path, opts).then(async (r) => {
    let data = {};
    try { data = await r.json(); } catch (e) { /* non-JSON */ }
    if (!r.ok) throw Object.assign(new Error((data && data.error) || ('HTTP ' + r.status)), { status: r.status, data });
    return data;
  });
}

function acctRender() {
  const { label } = acctEls();
  if (!label) return;
  const c = ACCT.current;
  if (c && c.authenticated) {
    const roleLabel = { GP: 'GP', LP: 'LP', MEMBER: 'Member', GUEST: 'Guest' }[c.role] || c.role;
    label.textContent = c.access ? (roleLabel + ' · ' + c.email) : ('Expired · ' + c.email);
  } else {
    label.textContent = 'Sign in';
  }
}

function acctOpen() {
  if (!ACCT.modal) return;
  ACCT.modal.showModal();
  const email = document.getElementById('acct-email');
  if (email) email.focus();
}

function acctClose() {
  if (ACCT.modal) ACCT.modal.close();
}

function acctToast(msg) {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.style.display = 'block';
  setTimeout(() => { t.style.display = 'none'; }, 4000);
}

async function acctRefresh() {
  try {
    ACCT.current = await acctFetch('/api/auth/me');
  } catch (e) {
    ACCT.current = { authenticated: false };
  }
  acctRender();
}

async function acctSendCode(email) {
  await acctFetch('/api/auth/request', { method: 'POST', body: JSON.stringify({ email }) });
}

async function acctVerify(email, code) {
  const res = await acctFetch('/api/auth/verify', { method: 'POST', body: JSON.stringify({ email, code }) });
  return res;
}

async function acctLogout() {
  await acctFetch('/api/auth/logout', { method: 'POST', body: '{}' });
  ACCT.current = { authenticated: false };
  acctRender();
  acctToast('Signed out');
}

function acctBind() {
  const root = document.getElementById('acct-modal');
  if (!root) return;
  const emailInput = root.querySelector('#acct-email');
  const codeInput = root.querySelector('#acct-code');
  const sendBtn = root.querySelector('#acct-send');
  const verifyBtn = root.querySelector('#acct-verify');
  const status = root.querySelector('#acct-status');
  const errorEl = root.querySelector('#acct-error');
  const logoutBtn = root.querySelector('#acct-logout');
  const subBtn = root.querySelector('#acct-subscribe');

  function setStatus(msg) { if (status) status.textContent = msg || ''; }
  function setError(msg) { if (errorEl) errorEl.textContent = msg || ''; }

  if (sendBtn) sendBtn.addEventListener('click', async () => {
    const email = (emailInput && emailInput.value || '').trim();
    if (!email || email.indexOf('@') < 1) { setError('Enter a valid email.'); return; }
    setError(''); setStatus('Sending code…');
    try {
      await acctSendCode(email);
      setStatus('Code sent to ' + email + '. Check your inbox (and the console log in dev).');
      if (codeInput) codeInput.focus();
    } catch (e) {
      setStatus(''); setError(e.message || 'Could not send code.');
    }
  });

  if (verifyBtn) verifyBtn.addEventListener('click', async () => {
    const email = (emailInput && emailInput.value || '').trim();
    const code = (codeInput && codeInput.value || '').trim();
    if (!email || !code) { setError('Enter email and the code from your inbox.'); return; }
    setError(''); setStatus('Verifying…');
    try {
      await acctVerify(email, code);
      acctClose();
      acctRefresh();
      acctToast('Signed in as ' + email);
    } catch (e) {
      setStatus(''); setError(e.message || 'Code was invalid or expired.');
    }
  });

  if (logoutBtn) logoutBtn.addEventListener('click', () => {
    acctLogout();
    acctClose();
  });

  if (subBtn) subBtn.addEventListener('click', async () => {
    const c = ACCT.current;
    if (!c || !c.authenticated || !c.email) { setError('Sign in first.'); return; }
    setError(''); setStatus('Subscribing…');
    try {
      await acctFetch('/api/auth/subscribe', { method: 'POST', body: JSON.stringify({ email: c.email }) });
      await acctRefresh();
      acctToast('You are now a subscription member.');
      acctClose();
    } catch (e) {
      setStatus(''); setError(e.message || 'Could not subscribe.');
    }
  });

  const closeBtn = root.querySelector('#acct-close');
  if (closeBtn) closeBtn.addEventListener('click', acctClose);
}

function acctInit() {
  const btn = document.getElementById('acct-btn');
  const modal = document.getElementById('acct-modal');
  if (!btn && !modal) return;
  if (btn) btn.addEventListener('click', () => {
    if (ACCT.current && ACCT.current.authenticated) {
      // clicking the account pill opens the modal to manage the account
      acctOpen();
    } else {
      acctOpen();
    }
  });
  ACCT.modal = modal;
  acctBind();
  acctRefresh();
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', acctInit);
  } else {
    acctInit();
  }
}
