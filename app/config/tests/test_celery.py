from django.test import TestCase

from celery.result import AsyncResult
from celery.exceptions import TimeoutError

from app.config.celery import debug_task


class TestCelery(TestCase):
    def test_debug_task(self):
        result = debug_task.delay()

        self.assertIsInstance(result, AsyncResult)

        try:
            result = result.get(timeout=1)
            self.assertEqual(result, "Celery works!")
        except TimeoutError:
            self.fail("Celery task took too long to complete")
