import requests
from flask import current_app, request
from . import api_blueprint


def users_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["NC_USER_HOST"],
        current_app.config["NC_USER_PORT"],
        route)


# - Get collection of all users
# - Post user
@api_blueprint.route(
    "/users",
    methods=["GET", "POST"])
def users():

    uri = users_uri("users")

    if request.method == "GET":

        # TODO This requires the admin API key!
        response = requests.get(uri)

    elif request.method == "POST":

        response = requests.post(uri, json=request.get_json())


    return response.text, response.status_code


# - Get user by id
@api_blueprint.route(
    "/users/<uuid:user_id>",
    methods=["GET"])
def user(
        user_id):
    uri = users_uri("users/{}".format(user_id))
    response = requests.get(uri)

    return response.text, response.status_code
