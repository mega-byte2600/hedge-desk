# Emporion demo runbook

Everything below is verified working on the combined branch (`combine/all-verified`, PR #42).

## 0. One-time prep (5 minutes, before the demo)

Pick **one** of these:

**A. Demo from this Mac (works today, no deploys)**
```bash
cd ~/workspace/projects/hedge-desk
git checkout combine/all-verified
bash scripts/demo.sh
# open http://127.0.0.1:8765
```
Sign-in codes print to the terminal (dev mail fallback) — copy the code from the
terminal into the modal. Set `GP_EMAIL=you@yourhost.com` to be the GP.

**B. Demo the public Render URL (needs the merge)**
Merge PR #42 → Render auto-deploys main → https://hedge-desk.onrender.com

## 1. The 5-minute demo script

| # | Do this | Say / what it proves |
|---|---|---|
| 1 | Open the console (`/`) | The desk is **open** — guests can explore, nothing is hidden behind a wall. |
| 2 | Point at the footer timestamp | The report is **recomputed live from the engine**, not a frozen snapshot. Click **Reload snapshot** and watch the time change. |
| 3 | Click **About** → scroll to **Access & membership** | The three tiers are published openly: Guest (free, synthetic), Member (subscription, live data + your broker), LP (investor in the LLC — invited, never a paid tier). |
| 4 | **Sign in** (top right) → enter your email → **Send code** | Email-OTP sign-in. The code appears in the terminal. This is the first-party email list. |
| 5 | Enter the code → **Sign in** | You land as **Guest — test drive, 31 days left**. The tier line shows the countdown. |
| 6 | Click the account pill → **Broker connection** | For members/LPs: *Connect broker (read-only)*. Guests are denied — tier gating is visible. |
| 7 | Sign in as the GP (`GP_EMAIL`) | The **GP console** appears: LP seats used/cap (x/99), member counts, and invite-an-LP. |
| 8 | Invite an LP by email | A row is created with the LP role; the 99-seat cap is enforced server-side. |
| 9 | `/api/report` and `/api/tier` in a second tab (optional, for the technical audience) | Live JSON: the engine output and the caller's data entitlement. |

## 2. What to say if asked "is this real?"

- **Real:** the engine runs on demand (measured ~0.01s) and recomputes on load; the
  auth, tiers, invites, rate limits, and read-only broker scaffold are all implemented
  and covered by **531 passing tests**; CI is green (Python 3.9/3.11/3.13, scan, CodeQL,
  Golden Master, load/capacity).
- **Not real (by design, say so plainly):** no orders are placed. Broker access is
  **read-only**. Market data is synthetic fixtures. There is no live P&L. Real LP
  capital needs the fund structure + counsel first.

Saying the limits out loud reads as strength here — it is the same reason the desk's
risk gate is credible.

## 3. If something breaks mid-demo

- **Page hangs on first load:** Render free sleeps after ~15 min idle. Wait ~30s, or
  refresh — the console now shows "Waking the research desk…" instead of hanging.
- **No social buttons:** expected unless Supabase is configured. Email-OTP is the
  fallback and always works.
- **Broker section says "not configured":** expected until `SCHWAB_*` is set. It
  degrades cleanly; nothing else is affected.
- **Fall back:** `bash scripts/demo.sh` locally — independent of Render entirely.

## 4. After the demo (the real gates)

- Merge PR #42.
- Supabase project + `supabase/schema.sql`, then set `SUPABASE_URL`,
  `SUPABASE_SERVICE_KEY`, `MEMBERSHIP_SECRET`, `GP_EMAIL` on Render so members persist.
- Add an external uptime pinger (UptimeRobot / cron-job.org, free) so cold starts stop.
- **Securities counsel** before any live LP capital or order execution.
