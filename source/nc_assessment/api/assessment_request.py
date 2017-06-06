import requests
from flask import current_app, request
from . import api_blueprint


def assessment_requests_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["NC_ASSESSMENT_REQUEST_HOST"],
        current_app.config["NC_ASSESSMENT_REQUEST_PORT"],
        route)


# - Get collection of all assessment_requests
# - Post assessment request
@api_blueprint.route(
    "/assessment_requests",
    methods=["GET", "POST"])
def assessment_requests():

    uri = assessment_requests_uri("assessment_requests")

    if request.method == "GET":

        # TODO This requires the admin API key!
        response = requests.get(uri)

    elif request.method == "POST":

        response = requests.post(uri, json=request.get_json())


    return response.text, response.status_code


# - Get assessment request by id
@api_blueprint.route(
    "/assessment_requests/<uuid:id>",
    methods=["GET"])
def assessment_request(
        id):
    uri = assessment_requests_uri("assessment_requests/{}".format(id))
    response = requests.get(uri)

    return response.text, response.status_code
