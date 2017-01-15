# import json
import requests
from flask import current_app, flash, render_template, url_for
from . import dashboard


# def api_uri():
#     return "http://{}:{}/{}".format(
#         current_app.config["NC_ASSESSMENT_HOST"],
#         current_app.config["NC_ASSESSMENT_PORT"])


# def assessment_uri(
#         route):
#     return "http://{}:{}/{}".format(
#         current_app.config["NC_ASSESSMENT_HOST"],
#         current_app.config["NC_ASSESSMENT_PORT"],
#         route)


@dashboard.route("/")
def dashboard():

    # api = {
    #         "resources": {
    #             # "aggregate_methods": {
    #             #     "route": "/aggregate_methods"
    #             # },
    #             # "aggregate_queries": {
    #             #     "route": "/aggregate_queries"
    #             # }
    #         }
    #     }

    # api = json.dumps(api, sort_keys=True, indent=4, separators=(',', ': '))

    return render_template("index.html")  # , api=api)
