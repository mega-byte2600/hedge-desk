# Engineering lessons

Failure classes this project has actually hit, with the rule that prevents each. Rules, not
incident narration: when a failure repeats, the fix belongs here and in a test, not in a
reviewer's memory.

Each rule earned its place from real evidence in this repository: failing CI runs, restore
commits, or a bug that shipped and had to be fixed twice.

---

## 1. Locked public copy is not safe from a DOM edit

**What happened.** Positioned copy kept getting destroyed by changes to the structure around
it. Evidence:

- `544b4be` Restore RoR survival copy regression anchor (1 line, `web/professional.js`)
- `dec7f31` Restore RoR portfolio-survival positioning (20 insertions, 10 deletions)
- `9203feb` Preserve candidate explainer regression copy (1 line, `web/candidate-context.js`)
- a bare `querySelector('.ws-ror')` matched **two** blocks and rewrote the wrong one, so the
  coordinated-research-architecture block was replaced with portfolio-survival text
- 25 failed CI runs, clustered in one day of copy work: break, restore, lock, lock again

**Rule.** Copy that carries a claim (Risk of Ruin, positioning, disclaimers, method
descriptions) is a locked artefact. If you touch it or the DOM it sits in:

1. Select it by an explicit hook, never by a class that can belong to more than one block.
   A bare class selector is a bug waiting for the second element to exist.
2. Run the claim/lock regression tests before and after. If a lock test does not exist for
   the copy you are changing, add one first.
3. Never "improve" positioned copy in a refactor. Changing the words is a separate, declared
   change with the reason stated in the commit.

## 2. A check that passes for the wrong reason is worse than no check

`grep -c` counts matches, not the thing you think. Real miscounts: a code **comment** quoting
an old label read as "the copy is still live"; a **CSS class** (`soul-grid`) read as an
internal term leaking onto the page; a **language server** process read as a stale test run.

An SPA answers 200 for unknown paths, so a failure-path test pointed at a bogus URL proves
nothing. A cached, minute-resolution value cannot change inside its cache window, so "the
button did nothing" was wrong.

**Rule.** Before quoting a count as evidence, print *what* matched. Assert content or
behaviour, never a status code. When a test fails, decide whether the test or the app is
wrong before reporting a defect — an assertion is a hypothesis, not proof.

## 3. Do not park a testable path as "unverified"

"Unverified" is honest only when the means are genuinely absent: no credentials, no hardware,
no capability. With a local server and a browser running, listing a click path as a
limitation is a dodge, because the tool was in hand.

**Rule.** Before writing the word into a report, name the missing capability. If there is
none, run the test.

## 4. Operating the environment

- **A `pkill` pattern can match the launcher's own command line** and kill the process you
  just started. Use the bracket form (`pgrep -f '[c]loudflared'`) or kill by port via
  `lsof -t`. This cost a full 205-control sweep run.
- **Never restart a server while a long test is walking it.** The run dies mid-flight and its
  output is worthless. Same sweep, same day.
- **List scheduled jobs before creating one.** A duplicate keepalive was created for a site
  that already had a better one; two pingers then raced the same target.
- **Backticks inside a shell-quoted string are command substitution.** A PR body containing
  code spans gets mangled. Write the body to a file, pass `--body-file`.
- **Do not assume a tool's cached install is complete.** A Playwright cache entry existed
  with no browsers downloaded. Validate launchability before trusting the tool.

## 5. Threading and the web server

**What happened.** A `sqlite3.connect` handle was created with the default
`check_same_thread=True` while the server runs a threaded WSGI server, so requests from other
threads raised and the sign-in code path returned 500s. It looked like an email problem.

**Rule.** Every store opened for a web server must be thread-safe by construction: one
connection per operation (or an explicit lock), opened with cross-thread use in mind. Prove
it with concurrent requests, not a single-threaded unit test.

## 6. Long-running observers

**What happened twice.** A `MutationObserver` callback wrote into its own observed subtree
with no guard, so it re-entered itself forever and froze the main thread. Once in
`ror-positioning.js`, once in `multi-agent-desk.mjs`. The page rendered and ignored every
click, which reads as "broken layout" rather than "frozen thread".

**Rule.** Any observer callback that writes to its observed subtree must be idempotent and
deferred (`requestAnimationFrame`), with a re-entrancy guard. A page that renders but ignores
input is a frozen thread: probe responsiveness before re-checking selectors.

## 7. Financial arithmetic

**Rule.** Money and approval ratios use `Decimal`. Every financial primitive gets exact
hand-computable reference cases (a par bond prices at exactly 1000.00; a 5-wide credit spread
at 2.60 credit risks exactly 240.00 per contract). A plausible-looking number is not a test.
Agents never compute, infer, or substitute a Risk of Ruin value.

## 8. Reporting

**Rule.** Report the **diff**, measured the same way before and after, and state what did not
move. "Gap 0px to 16px, and the neighbouring element moved by exactly the same 16px" is
proof of blast radius. "Looks fine now" is not. Where a change cannot be verified by the
means at hand, say which capability is missing rather than gesturing at uncertainty.

Also: never claim a fix is live until the deployed artefact has been re-measured. Merged is
not deployed, and deployed is not correct.
