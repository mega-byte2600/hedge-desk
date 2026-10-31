"""Daily-brief page copy regression guard.

Incident (found 2026-10-24, Saturday polish): the Daily brief page told
readers its research input came from "the six desks" and was "Replaced every
morning". Both were false. The daily research pipeline runs seven desks
(the repo registry lists six working desks plus Bonds & Rates), and the
research run publishes in the afternoon (13:30 PT run), not the morning.
This test pins the corrected copy so the drift cannot silently return.

Scope note: the Candidates page's "six desk methods" / "Six-desk candidate
board" copy is deliberately NOT covered here — it describes the six
evaluated workflows, a different (defensible) count, and is left alone.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_JS = ROOT / "web" / "app.js"


def test_brief_page_states_seven_desks_and_afternoon_refresh():
    text = APP_JS.read_text(encoding="utf-8")
    assert "from the seven desks. Replaced every afternoon." in text
    assert "after the afternoon research run" in text


def test_brief_page_does_not_repeat_the_stale_claims():
    lowered = APP_JS.read_text(encoding="utf-8").lower()
    assert "six desks" not in lowered
    assert "every morning" not in lowered
    assert "morning research run" not in lowered
