from django.test import TestCase

from celery.result import AsyncResult
from celery.exceptions import TimeoutError

from ..tasks import send_notification_email


class TestTasks(TestCase):
    def test_send_notification_email(self):
        subject = "Test subject"
        message = "Test message"
        recipients = ["josueisai@gmail.com"]
        result = send_notification_email.delay(subject, message, recipients)  # type: ignore
        self.assertIsInstance(result, AsyncResult)

        try:
            result = result.get(timeout=10)
            expected = f"Email sent to {', '.join(recipients)} successfully."
            self.assertEqual(result, expected, f"Expected: {expected}, got: {result}")
        except TimeoutError:
            self.fail("Task execution timed out")
