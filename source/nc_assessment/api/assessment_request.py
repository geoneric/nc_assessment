import json
import requests
from flask import current_app, request
import pika
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

        if response.status_code == 201:
            # Ask for assessment of the effects on natural capital. This
            # creates the data we can later visualize in the webapp.

            request_dict = response.json()["assessment_request"]
            assert request_dict["status"] == "pending", request_dict["status"]
            request_uri = assessment_requests_uri(
                request_dict["_links"]["self"])

            # Mark request's status as 'queued'
            payload = {
                "status": "queued"
            }
            response = requests.patch(request_uri, json=payload)

            if response.status_code == 200:

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
                    queue="perform_nca",
                    durable=True)
                channel.basic_publish(
                    exchange="",
                    routing_key="perform_nca",
                    # body=json.dumps(payload),
                    body="{}".format(request_uri),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Persistent messages.
                    )
                )
                connection.close()


    return \
        response.text, \
        201 if response.status_code == 200 else response.status_code


# - Get assessment request by id
@api_blueprint.route(
    "/assessment_requests/<uuid:id>",
    methods=["GET"])
def assessment_request(
        id):
    uri = assessment_requests_uri("assessment_requests/{}".format(id))
    response = requests.get(uri)

    return response.text, response.status_code
