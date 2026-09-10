/* Membership / auth UI for the Emporion desk.
 *
 * The research console stays open (guest "test drive" tier is public). This
 * adds an opt-in membership layer:
 *   - a Sign in / account control in the topbar,
 *   - social login via Supabase Auth (Google/GitHub/... IdP),
 *   - email-OTP sign-in (no password) as a fallback,
 *   - role-aware UI (guest / member / LP / GP),
 *   - self-serve subscription (MEMBER) and GP invite (LP) surfaces.
 *
 * Identity (email + provider) comes from Supabase Auth; the desk maps that
 * verified email to a membership role/tier. Email-OTP also captures a
 * verified, consent-collected email -> the GP's first-party marketing list.
 */

// Pinned to an exact version for supply-chain reproducibility (never @2 / @latest).
const SUPABASE_JS_CDN = 'https://esm.sh/@supabase/supabase-js@2.116.0';
let _supabaseClient = null;

async function loadSupabase(url, anonKey) {
  if (_supabaseClient) return _supabaseClient;
  const mod = await import(/* @vite-ignore */ SUPABASE_JS_CDN);
  _supabaseClient = mod.createClient(url, anonKey, {
    auth: { persistSession: true, detectSessionInUrl: true, autoRefreshToken: true },
  });
  return _supabaseClient;
}

const ACCT = {
  modal: null,
  current: null, // {authenticated, email, role, access, reason}
  tier: null, // {tier, real_data, investor}
  social: null, // {enabled, supabase_url, supabase_anon_key, providers}
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
  const t = ACCT.tier;
  if (c && c.authenticated) {
    const roleLabel = { GP: 'GP', LP: 'LP', MEMBER: 'Member', GUEST: 'Guest' }[c.role] || c.role;
    if (c.access) {
      const dataLabel = t && t.real_data ? ' · live data' : ' · test drive';
      label.textContent = roleLabel + dataLabel;
    } else {
      label.textContent = 'Expired · ' + c.email;
    }
  } else {
    label.textContent = 'Sign in';
  }
  // Reflect tier in the modal status line so users see what data they get.
  const tierLine = document.getElementById('acct-tier');
  if (tierLine) {
    if (!c || !c.authenticated) {
      tierLine.textContent = 'Browsing as a guest — synthetic test-drive data.';
    } else if (t && t.real_data) {
      tierLine.textContent = t.investor
        ? 'Investor access — live data and full desk service.'
        : 'Member access — live market data (broker link available).';
    } else {
      tierLine.textContent = 'Guest test drive — synthetic data. Upgrade for live data.';
    }
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
  try {
    ACCT.tier = await acctFetch('/api/tier');
  } catch (e) {
    ACCT.tier = null;
  }
  acctRender();
  acctBrokerRefresh();
}

/* ---- social login (Supabase Auth IdP) ---------------------------------- */

const PROVIDER_LABEL = {
  google: 'Continue with Google',
  github: 'Continue with GitHub',
  azure: 'Continue with Microsoft',
  apple: 'Continue with Apple',
};

async function acctLoadProviders() {
  try {
    ACCT.social = await acctFetch('/api/auth/providers');
  } catch (e) {
    ACCT.social = { enabled: false, providers: [] };
  }
  acctRenderProviders();
}

function acctRenderProviders() {
  const box = document.getElementById('acct-social');
  if (!box) return;
  const s = ACCT.social;
  if (!s || !s.enabled || !s.providers || !s.providers.length) {
    box.innerHTML = '';
    box.style.display = 'none';
    return;
  }
  box.style.display = 'block';
  box.innerHTML = s.providers
    .map((p) => `<button type="button" class="btn acct-social-btn" data-provider="${p}">${PROVIDER_LABEL[p] || ('Continue with ' + p)}</button>`)
    .join('');
  box.querySelectorAll('button[data-provider]').forEach((b) => {
    b.addEventListener('click', () => acctSocialSignIn(b.dataset.provider, b));
  });
}

async function acctSocialSignIn(provider, btn) {
  const s = ACCT.social;
  if (!s || !s.enabled) return;
  if (btn) { btn.disabled = true; }
  try {
    const client = await loadSupabase(s.supabase_url, s.supabase_anon_key);
    const { error } = await client.auth.signInWithOAuth({
      provider,
      options: { redirectTo: window.location.origin + window.location.pathname },
    });
    if (error) throw error;
  } catch (e) {
    if (btn) btn.disabled = false;
    const err = document.getElementById('acct-error');
    if (err) err.textContent = 'Social sign-in unavailable: ' + (e.message || e);
  }
}

/* After an OAuth redirect back, Supabase has a session in the URL/storage.
 * Exchange its access token with the desk to get our role-scoped session. */
async function acctCompleteSocialIfPresent() {
  const s = ACCT.social;
  if (!s || !s.enabled) return false;
  try {
    const client = await loadSupabase(s.supabase_url, s.supabase_anon_key);
    const { data } = await client.auth.getSession();
    const session = data && data.session;
    if (!session || !session.access_token) return false;
    await acctFetch('/api/auth/social', {
      method: 'POST',
      body: JSON.stringify({ access_token: session.access_token }),
    });
    await client.auth.signOut();
    await acctRefresh();
    acctToast('Signed in as ' + (ACCT.current && ACCT.current.email ? ACCT.current.email : ''));
    return true;
  } catch (e) {
    return false;
  }
}

/* ---- broker linking (read-only; members/LPs) ---------------------------- */

async function acctBrokerRefresh() {
  const box = document.getElementById('acct-broker');
  if (!box) return;
  const c = ACCT.current;
  if (!c || !c.authenticated || !(ACCT.tier && ACCT.tier.real_data)) {
    box.style.display = 'none';
    return;
  }
  box.style.display = 'block';
  let st = { configured: false, linked: false };
  try { st = await acctFetch('/api/broker/status'); } catch (e) { /* leave defaults */ }
  ACCT.broker = st;
  const label = document.getElementById('acct-broker-label');
  const connect = document.getElementById('acct-broker-connect');
  const disconnect = document.getElementById('acct-broker-disconnect');
  if (label) {
    label.textContent = !st.configured
      ? 'Broker linking is not configured on this deployment.'
      : (st.linked ? 'Broker connected (read-only).' : 'No broker connected yet.');
  }
  if (connect) connect.style.display = st.configured && !st.linked ? 'inline-flex' : 'none';
  if (disconnect) disconnect.style.display = st.linked ? 'inline-flex' : 'none';
}

async function acctBrokerConnect(btn) {
  if (btn) btn.disabled = true;
  try {
    const res = await acctFetch('/api/broker/authorize');
    if (res && res.authorize_url) { window.location.href = res.authorize_url; return; }
    throw new Error('no authorize url');
  } catch (e) {
    if (btn) btn.disabled = false;
    const err = document.getElementById('acct-error');
    if (err) err.textContent = 'Could not start broker link: ' + (e.message || e);
  }
}

async function acctBrokerDisconnect() {
  try { await acctFetch('/api/broker/unlink', { method: 'POST', body: '{}' }); } catch (e) { /* ignore */ }
  acctBrokerRefresh();
  acctToast('Broker disconnected');
}

/* The broker OAuth redirect returns ?code=...&state=... — finish the link. */
async function acctBrokerCompleteIfPresent() {
  const params = new URLSearchParams(window.location.search);
  const code = params.get('code');
  const state = params.get('state');
  if (!code || !state) return false;
  try {
    await acctFetch('/api/broker/link', {
      method: 'POST',
      body: JSON.stringify({ code, state }),
    });
    const url = new URL(window.location.href);
    url.searchParams.delete('code');
    url.searchParams.delete('state');
    window.history.replaceState({}, '', url.pathname + url.search + url.hash);
    acctToast('Broker connected (read-only)');
    acctBrokerRefresh();
    return true;
  } catch (e) {
    const err = document.getElementById('acct-error');
    if (err) err.textContent = 'Broker link failed: ' + (e.message || e);
    return false;
  }
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

  const bc = root.querySelector('#acct-broker-connect');
  if (bc) bc.addEventListener('click', () => acctBrokerConnect(bc));
  const bd = root.querySelector('#acct-broker-disconnect');
  if (bd) bd.addEventListener('click', acctBrokerDisconnect);
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
  acctLoadProviders().then(() => acctCompleteSocialIfPresent());
  acctBrokerCompleteIfPresent();
  acctRefresh();
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', acctInit);
  } else {
    acctInit();
  }
}
