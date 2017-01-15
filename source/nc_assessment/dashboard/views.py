import requests
from flask import current_app, flash, render_template, url_for
from . import dashboard


def plans_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["NC_PLAN_HOST"],
        current_app.config["NC_PLAN_PORT"],
        route)


@dashboard.route("/")
def dashboard():

    plans = []

    try:
        uri = plans_uri("plans")
        response = requests.get(uri)
        plans = response.json()
    except Exception as exception:
        flash("error contacting plan service: {}".format(exception))


    return render_template("index.html",
        plans=plans)
