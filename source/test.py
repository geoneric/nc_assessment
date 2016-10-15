import unittest
from flask import json
import nc_assessment


class TestCase(unittest.TestCase):

    def setUp(self):
        nc_assessment.app.config["TESTING"] = True
        self.app = nc_assessment.app.test_client()


    def tearDown(self):
        del self.app


    def test_ping(self):
        response = self.app.get("/ping")
        data = response.data.decode("utf8")
        self.assertEqual(response.status_code, 200, data)
        data = json.loads(data)
        self.assertEqual(data, {"response": "pong"})


if __name__ == "__main__":
    unittest.main()
