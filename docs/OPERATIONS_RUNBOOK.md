# Emporion Operations Runbook

Support document for running the Emporion / Hedge Desk console in front of people. It is
written for the operator (the GP), not for developers. Nothing here changes the product;
everything here is procedure.

Companion documents: `docs/DEMO_RUNBOOK.md` (demo script and what to click),
`docs/CONSOLE_VV_SPEC.md` (the verification spec and how to run it).

---

## 1. What is live, and what each URL is for

| URL | What it is | Use it for | Depends on |
| --- | --- | --- | --- |
| `https://hedge-desk.onrender.com` | **Production host.** Render free tier. | Anything you would send to another person. | Render account; Render's free tier sleeping after ~15 min idle. |
| `https://astra-mini.tail16a2cd.ts.net:8443` | **Stable demo URL.** Tailscale Funnel from this Mac. Verified publicly reachable. | Your own checking, and demoing with sign-in while Render email is unconfigured. | This Mac staying awake and the demo server running. |
| `https://here-enb-exotic-node.trycloudflare.com` | **Ephemeral backup.** Cloudflare quick tunnel. | Emergencies only. The name changes on every restart. | Same as above, plus the `cloudflared` process. |

Rule of thumb: **Render for anything you share; the funnel URL for anything you want to
click yourself right now.** The two tunnel URLs are conveniences that depend on the Mac
in this office; Render is the one that is actually hosted.

---

## 2. Resource map

Processes on this Mac (verify with `ps -eo rss,pid,command | grep -E 'cloudflared|demo|hedge'`):

| Process | Purpose | Typical memory |
| --- | --- | --- |
| `python -m hedge_desk.server` (port 8765) | The demo server | ~25 MB |
| `cloudflared tunnel` | Ephemeral backup URL only | ~45 MB |
| `scripts/demo_watchdog.sh` | Restarts the server if it stops answering | ~2 MB |
| `caffeinate -i` | Blocks idle sleep while the demo should be up | ~3 MB |
| Hermes gateway (`ai.hermes.gateway`, launchd agent) | Runs the scheduled keepalive | shared |

Files that matter:

| Path | What it is |
| --- | --- |
| `/tmp/hd-demo-live.db` | Demo members/audit store (SQLite). Delete it to reset the demo. |
| `/tmp/hd-demo-merged.log` | Demo server request log |
| `/tmp/hd-watchdog.log` | Watchdog restarts, timestamps |
| `~/.hermes/scripts/hedge-desk-keepalive.sh` | The Render keepalive ping |
| `~/.hermes/cron/jobs.json` | Scheduled jobs (Hermes scheduler, **not** a Unix crontab) |

---

## 3. Start, stop, restart

**Demo server (funnel URL):**

```bash
cd ~/workspace/projects/hedge-desk
PORT=8765 MEMBERSHIP_DB=/tmp/hd-demo-live.db \
  GP_EMAIL=<the GP address> MEMBERSHIP_SECRET=<a local secret> \
  bash scripts/demo.sh
```

**Stop it** (and, because the watchdog would restart it, stop the watchdog first):

```bash
pkill -f demo_watchdog.sh      # stop the watchdog, otherwise it resurrects the server
lsof -nP -iTCP:8765 -t | xargs kill
```

**Restart cleanly:** stop as above, then start as above. Never `pkill -f hedge_desk.server`
from the same command that launches a new server — the pattern matches the launcher's own
command line and kills the new process. This mistake cost one full sweep run.

**Reset the demo data:** stop the server, `rm /tmp/hd-demo-live.db`, start it again.

---

## 4. Health checks

```bash
curl -sS -m 10 https://hedge-desk.onrender.com/api/health
```

Expect `"status": "ok"`, `"mode": "paper"`, and `"live_orders_enabled": false`. **If
`live_orders_enabled` is ever `true`, treat it as an incident** — the product is meant to
be paper-only, and something has changed that nobody intended.

Slow response pattern (`http 200` but 12-60s) means the Render instance was asleep. Warm it
with `curl -m 120` and retry; it is not an outage.

---

## 5. Monitoring, and how you find out something broke

- **Render keepalive** — a Hermes scheduled job (`no_agent`, every 8 min) curls `/`,
  `/api/health`, and `/report.json` so the first visitor gets a warm instance. Silent when
  healthy; it alerts to your connected channels on a non-200.
- **Local watchdog** — every 45s checks the demo server and restarts it if it stops
  answering, and holds off idle sleep.

Two honest limits:

1. These are **local** jobs. If this Mac is asleep or off, pings pause until it wakes.
   True 24/7 independence needs an always-on third party.
2. Keeping a free-tier Render instance permanently warm consumes essentially the entire
   free allowance (750 instance-hours/month against ~730 in a month). It fits exactly one
   service. Watch the Render dashboard if a second service is ever added.

---

## 6. Before every demo — pre-flight

Run these in order; each should pass before you send anyone a link.

```bash
# 1. is the host awake and in paper mode?
curl -sS -m 30 -o /dev/null -w '%{http_code}\n' https://hedge-desk.onrender.com/

# 2. does the page actually render, not just answer?
cd ~/workspace/projects/hedge-desk
node scripts/smoke_console.mjs https://hedge-desk.onrender.com

# 3. is sign-in working on the URL you plan to show?
#    (Render needs SMTP_* configured; the funnel URL works today)
```

- Open the URL in a **fresh private window** so a stale cache cannot fool you.
- Click: each of the 8 tabs, one desk from the Research desks tab, one scenario row, and
  submit a Yellow Sheet. Those are the paths that have broken before.
- Have the fallback URL ready. If the primary is cold, waiting 30-60s fixes it; say so out
  loud rather than letting a pause look like a failure.
- Decide in advance what you will *not* claim: see section 9.

---

## 7. Incident playbook

| Symptom | Most likely cause | Action |
| --- | --- | --- |
| Site loads after a long pause | Render idle sleep | Wait 30-60s, reload. Not an outage. |
| Blank page / frozen tab | A render loop | Reload. If repeatable, report it — this class of bug has shipped twice and both times came from a MutationObserver callback writing to its own observed subtree. |
| "Code sent" but no email | `SMTP_*` unset on Render | Use the funnel URL, or complete the Render email configuration (section 8). The code is visible in the Render log meanwhile. |
| Members/invites vanished | Supabase not configured | Expected on free tier: state resets on redeploy. Configure Supabase (section 8) for durable membership. |
| Funnel URL dead | Mac asleep, or server/watchdog stopped | Restart the server (section 3); the watchdog should have done it — check `/tmp/hd-watchdog.log`. |
| `exotic-node` URL dead | `cloudflared` stopped | Restart `cloudflared tunnel --url http://127.0.0.1:8765`; a **new** hostname is issued. |
| Sign-in says a tier changed | Regression | Stop the demo and report it. Tier changes were fixed once already (`SignInMustNotDowngradeTests`). |

---

## 8. Configuration gaps and how to close them

Current state, honestly:

| Setting | State | Consequence | To close it |
| --- | --- | --- | --- |
| `GP_EMAIL` | Set locally, unset on Render | GP console lane not addressable on Render | Set it in Render → Environment |
| `SMTP_*` | Unset everywhere | Emailed codes reach only the service log | Set SMTP host/port/user/password on Render |
| `SUPABASE_URL` / anon key | Unset | Social login off; member state resets per deploy | Create a Supabase project, set both, then the auth path is live |
| `SCHWAB_*` | Unset | Broker connect is inert (by design, paper-only) | Only when read-only brokerage access is deliberately released |

Setting Render environment variables requires `render login` once on this machine — about
30 seconds of your time, then the GP console and email delivery work on the real host.

---

## 9. What must never be claimed

The product's own boundary language, from the shipped disclosures (`web/disclosures.json`):

- Paper only. **No orders can be placed.** Nothing here trades.
- Research output is not investment advice, not a recommendation, and not an offer to sell
  any security.
- The guest/demo tier runs on synthetic fixtures, not live market data.
- The console does not calculate, estimate, or validate a Risk of Ruin figure. Any RoR
  value must come from the separately versioned deterministic component.
- No performance history exists and none may be implied. Positioning is stated as
  capability, never as performance.

If a sentence would sound like a promise of returns, it does not go on a slide.

---

## 10. Credentials policy

- No secrets, credentials, or personal data in the repository, commits, PR bodies, issues,
  or logs. The repository is public.
- The demo instance uses a **synthetic** membership secret and a local SQLite store; it
  holds no real member data.
- Environment values live only in the process environment or the Render dashboard. This
  document deliberately names variables, never values.

---

## 11. Escalation

Bring the operator (the GP) in when: sign-in or tier behaviour changes, anything suggests
live order capability, or the disclosure language above stops being true.

When reporting a problem, send: the URL, what you clicked, what you expected, what you saw,
and whether a reload changed it. That is enough to reproduce almost everything.
