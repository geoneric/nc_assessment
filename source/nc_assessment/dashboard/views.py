import requests
from flask import current_app, flash, render_template
from . import dashboard


def assessment_requests_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["NC_ASSESSMENT_REQUEST_HOST"],
        current_app.config["NC_ASSESSMENT_REQUEST_PORT"],
        route)


def plans_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["NC_PLAN_HOST"],
        current_app.config["NC_PLAN_PORT"],
        route)


def users_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["NC_USER_HOST"],
        current_app.config["NC_USER_PORT"],
        route)


def get_resource(
        uri_generator,
        route):

    resource = []

    try:

        uri = uri_generator(route)
        response = requests.get(uri)

        if response.status_code != 200:
            flash("error getting resource: {}".format(route))
        else:
            resource = response.json()

    except Exception as exception:
        flash("error contacting service: {}".format(exception))

    return resource


@dashboard.route("/")
def dashboard():

    assessment_indicator_results = get_resource(
        assessment_requests_uri, "assessment_indicator_results")
    assessment_requests = get_resource(
        assessment_requests_uri, "assessment_requests")
    assessment_results = get_resource(
        assessment_requests_uri, "assessment_results")
    plans = get_resource(plans_uri, "plans")
    users = get_resource(users_uri, "users")


    return render_template("index.html",
        assessment_indicator_results=assessment_indicator_results,
        assessment_requests=assessment_requests,
        assessment_results=assessment_results,
        plans=plans,
        users=users
    )
