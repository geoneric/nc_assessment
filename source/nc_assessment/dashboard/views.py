import requests
from flask import current_app, flash, render_template, url_for
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


@dashboard.route("/")
def dashboard():

    assessment_requests = []

    try:
        uri = assessment_requests_uri("assessment_requests")
        response = requests.get(uri)
        assessment_requests = response.json()
    except Exception as exception:
        flash("error contacting assessment request service: {}".format(
            exception))


    plans = []

    try:
        uri = plans_uri("plans")
        response = requests.get(uri)
        plans = response.json()
    except Exception as exception:
        flash("error contacting plan service: {}".format(exception))


    users = []

    try:
        uri = users_uri("users")
        response = requests.get(uri)
        users = response.json()
    except Exception as exception:
        flash("error contacting user service: {}".format(exception))


    return render_template("index.html",
        assessment_requests=assessment_requests,
        plans=plans,
        users=users
    )
