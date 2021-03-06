import unittest
from flask import current_app, json
from nc_assessment import create_app


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True
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
                    "assessment_indicator_results": {
                        "route": "/assessment_indicator_results"
                    },
                    "assessment_requests": {
                        "route": "/assessment_requests"
                    },
                    "assessment_results": {
                        "route": "/assessment_results"
                    },
                    "lu_classes": {
                        "route": "/lu_classes"
                    },
                    "plans": {
                        "route": "/plans"
                    },
                    "users": {
                        "route": "/users"
                    },
                }
            })


if __name__ == "__main__":
    unittest.main()
