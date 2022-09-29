# project/server/tests/test_api.py
import unittest

from base import BaseTestCase


class TestApiBlueprint(BaseTestCase):
    def test_hello(self):
        # Ensure Flask is setup.
        response = self.client.get("/api/hello", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"world", response.data)


if __name__ == "__main__":
    unittest.main()
