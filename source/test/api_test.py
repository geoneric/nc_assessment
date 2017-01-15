import unittest
from flask import current_app, json
from nc_assessment import create_app


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()

        self.app_context.push()

        self.client = self.app.test_client()


    def tearDown(self):
        self.app_context.pop()


    def test_api(self):
        response = self.client.get("/api")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, data)

        data = json.loads(data)

        self.assertEqual(data, {
                "resources": {
                    "plans": {
                        "route": "/plans"
                    },
                }
            })


if __name__ == "__main__":
    unittest.main()
