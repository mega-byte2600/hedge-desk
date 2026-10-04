import unittest

from hedge_desk.email_transport import SmtpSender


class EmailTransportTests(unittest.TestCase):
    def test_unconfigured_sender_fails_closed_without_logging_otp(self):
        sender = SmtpSender({})
        self.assertFalse(sender.configured)
        with self.assertRaisesRegex(RuntimeError, "not configured"):
            sender.send(
                "user@example.com",
                "Your Emporion desk sign-in code",
                "Your one-time sign-in code is:\n\nSUPER-SECRET-OTP",
            )


if __name__ == "__main__":
    unittest.main()
