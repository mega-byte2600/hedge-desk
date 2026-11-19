import pytest

from hedge_desk.data.feed_base import RETRYABLE_STATUSES, with_retries


def _seq(*responses):
    calls = []

    def transport(url):
        calls.append(url)
        return responses[min(len(calls) - 1, len(responses) - 1)]

    return transport, calls


def test_retries_transient_then_succeeds_with_bounded_jittered_sleep():
    t, calls = _seq((503, b""), (0, b"reset"), (200, b"ok"))
    sleeps = []
    wrapped = with_retries(t, attempts=3, base_delay=1.0, sleeper=sleeps.append, rng=lambda: 0.5)
    assert wrapped("u") == (200, b"ok")
    assert len(calls) == 3
    assert sleeps == [0.5, 1.0]  # full jitter: rng * base * 2**(n-1)


def test_does_not_retry_client_errors_and_returns_last_response():
    t, calls = _seq((404, b"nope"))
    assert with_retries(t, sleeper=lambda s: None)("u") == (404, b"nope")
    assert len(calls) == 1


def test_gives_up_after_attempts_and_keeps_fail_closed_status():
    t, calls = _seq((500, b"x"))
    assert with_retries(t, attempts=3, sleeper=lambda s: None)("u")[0] == 500
    assert len(calls) == 3


def test_policy_and_validation():
    assert {429, 500, 502, 503, 504, 0} == set(RETRYABLE_STATUSES)
    with pytest.raises(ValueError):
        with_retries(lambda u: (200, b""), attempts=0)
