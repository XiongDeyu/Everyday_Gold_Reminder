import io
import json
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

import gold_reminder_agent as agent


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class GoldReminderAgentTests(unittest.TestCase):
    @patch("gold_reminder_agent.urlopen")
    def test_fetch_gold_price_parses_price(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"price": 2375.12})

        price = agent.fetch_gold_price()

        self.assertEqual(price, 2375.12)

    @patch("gold_reminder_agent.urlopen")
    def test_fetch_gold_price_raises_when_missing_price(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"unexpected": 1})

        with self.assertRaises(ValueError):
            agent.fetch_gold_price()

    def test_build_reminder_message_with_threshold(self):
        now = datetime(2026, 5, 12, tzinfo=timezone.utc)

        msg = agent.build_reminder_message(
            price=2400.00,
            threshold=2300.00,
            now=now,
        )

        self.assertIn("2026-05-12", msg)
        self.assertIn("已达到你设置的提醒阈值 2300.00", msg)

    def test_run_daily_reminder_uses_notifier(self):
        output = io.StringIO()

        def notifier(message):
            output.write(message)

        message = agent.run_daily_reminder(notifier=notifier, mock_price=2200.0)

        self.assertEqual(output.getvalue(), message)
        self.assertIn("今日金价提醒", message)


if __name__ == "__main__":
    unittest.main()
