from flask import Flask, jsonify, request
from flask.json import dumps
import pika


app = Flask(__name__)
app.config.from_object("nc_assessment.default_settings")


@app.route("/ping")
def ping():
    return jsonify(response="pong"), 200


@app.route("/register_plan",
        methods=["POST"])
def register_plan():
    """
    Register a land-use plan with the geodatabase

    This call is asynchronous. Sometime in the future, the plan will be
    registered. If so, a WMC end-point will be available for it, so you
    can visualize it.
    """
    data = request.get_json()
    id = data["id"]
    name = data["name"]
    app.logger.debug(dumps({
        "nc_route": "register_plan",
        "nc_id": id,
        "nc_name": name
    }))

    # Add a message to the message broker asking for the registration of
    # the plan.

    queue_name = "register_plan"
    message = dumps({
        "id": id,
        "name": name
    })

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host="rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode = 2, # make message persistent
        )
    )
    connection.close()

    return jsonify({
        "_links": {
            "wms_plan": {
                "href": "wms_plan"
            }
        }
    }), 201


@app.route("/wms_plan",
        methods=["GET"])
def wms_plan():
    """
    Ask for WMS end point for the plan uploaded during session with the id
    passed in

    This call is synchronous. It will wait until the WMS end-point
    is available, or the timeout has passed.
    """
    data = request.get_json()
    id = data["id"]

    return jsonify({
        "link": "blah"
    }), 200
