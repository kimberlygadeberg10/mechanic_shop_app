import unittest
from flask_app import app


class TestMechanicRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()