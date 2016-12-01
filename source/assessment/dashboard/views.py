import requests
from flask import current_app, flash, jsonify, render_template, url_for
from . import dashboard


# def aggregate_queries_uri(
#         route):
#     return "http://{}:{}/{}".format(
#         current_app.config["AGGREGATE_QUERY_HOST"],
#         current_app.config["AGGREGATE_QUERY_PORT"],
#         route)


@dashboard.route("/")
def dashboard():

    # # TODO Handle errors.
    # uri = aggregate_queries_uri("aggregate_methods")
    # response = requests.get(uri)
    # methods = response.json()

    # uri = aggregate_queries_uri("aggregate_queries")
    # response = requests.get(uri)
    # queries = response.json()

    return render_template("index.html")  # , methods=methods, queries=queries)
