import json
import requests
import traceback
from werkzeug.exceptions import *
from flask import current_app, jsonify, request
from flask_uploads import UploadNotAllowed
import pika
from . import api_blueprint
from .. import uploaded_plans


def plans_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["NC_PLAN_HOST"],
        current_app.config["NC_PLAN_PORT"],
        route)


# - Post a plan
# - Get collection of all plans
@api_blueprint.route(
    "/plans",
    methods=["GET", "POST"])
def plans_all():
    uri = plans_uri("plans")

    if request.method == "GET":

        # TODO This requires the admin API key!
        response = requests.get(uri)

    elif request.method == "POST":
        # The data passed in should contain a graphics file or dataset and a
        # JSON snippet with some additional information.
        # We must do the folowing:
        # - Grab the user's id
        # - Save the file
        # - Post some metadata to the plan service
        # - Post a message to the queue of plans to request the import
        #     into the geodatabase

        # After the plan is imported, information in the plans resource
        # can be requested by the client.

        try:
            data = json.loads(request.form["data"])
            # request.files["plan"] -> FileStorage
            # request.files["plan"].name -> plan
            # request.files["plan"].filename -> plan.png
            filename = uploaded_plans.save(
                request.files["plan"], folder=data["user"])
            pathname = uploaded_plans.path(filename)

            # Post snippet of JSON asking for the import of the graphics
            # file into the geodatabase. We expect to be notified when
            # this has happened.
            # `| user* | pathname | status | create_timestamp | last_edit_timestamp | wms_uri |`
            payload = {
                "user": data["user"],
                "pathname": pathname,
                "status": "uploaded"
            }

            response = requests.post(uri, json={"plan": payload})

            if response.status_code == 201:
                # Ask for the registration of the plan. This turns the
                # graphics files into rasters which can be visualized as a
                # map.

                plan_dict = response.json()["plan"]
                payload = {
                    "uri": plans_uri(plan_dict["_links"]["self"]),
                    "workspace": data["user"]
                }

                # Post message in rabbitmq and be done with it.
                credentials = pika.PlainCredentials(
                    current_app.config["NC_RABBITMQ_DEFAULT_USER"],
                    current_app.config["NC_RABBITMQ_DEFAULT_PASS"]
                )

                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host="rabbitmq",
                        virtual_host=current_app.config[
                            "NC_RABBITMQ_DEFAULT_VHOST"],
                        credentials=credentials,
                        # Keep trying for 8 minutes.
                        connection_attempts=100,
                        retry_delay=5  # Seconds
                ))
                channel = connection.channel()

                channel.queue_declare(
                    queue="register_raster",
                    durable=True)
                channel.basic_publish(
                    exchange="",
                    routing_key="register_raster",
                    body=json.dumps(payload),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Persistent messages.
                    )
                )
                connection.close()

        except UploadNotAllowed:
            raise BadRequest("uploading {} not allowed".format(
                request.files["plan"]))
        except Exception as exception:
            raise BadRequest(
                "invalid upload request, exception: {}, form: {}, "
                "files: {}".format(traceback.format_exc(), request.form,
                    request.files))


    return response.text, response.status_code


# - Get plan by user-id and plan-id
@api_blueprint.route(
    "/plans/<uuid:user_id>/<uuid:plan_id>",
    methods=["GET"])
def plan(
        user_id,
        plan_id):

    uri = plans_uri("plans/{}/{}".format(user_id, plan_id))
    response = requests.get(uri)

    return response.text, response.status_code


# - Post request for georeferencing a plan by user-id and plan-id
@api_blueprint.route(
    "/plans/<uuid:user_id>/<uuid:plan_id>/georeference",
    methods=["POST"])
def georeference_plan(
        user_id,
        plan_id):

    uri = plans_uri("plans/{}/{}".format(user_id, plan_id))
    # response = requests.get(uri)

    # if response.status_code == 200:

    data = request.get_json()
    payload = data["georeference"]
    payload["uri"] = uri

    # Post message in rabbitmq and be done with it.
    credentials = pika.PlainCredentials(
        current_app.config["NC_RABBITMQ_DEFAULT_USER"],
        current_app.config["NC_RABBITMQ_DEFAULT_PASS"]
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="rabbitmq",
            virtual_host=current_app.config[
                "NC_RABBITMQ_DEFAULT_VHOST"],
            credentials=credentials,
            # Keep trying for 8 minutes.
            connection_attempts=100,
            retry_delay=5  # Seconds
    ))
    channel = connection.channel()

    channel.queue_declare(
        queue="georeference_raster",
        durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="georeference_raster",
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Persistent messages.
        )
    )
    connection.close()

    return "request posted", 201


# - Get plans by user-id
@api_blueprint.route(
    "/plans/<uuid:user_id>",
    methods=["GET"])
def plans(
        user_id):

    uri = plans_uri("plans/{}".format(user_id))
    response = requests.get(uri)

    return response.text, response.status_code
