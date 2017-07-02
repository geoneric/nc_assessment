from flask import Flask, jsonify
from flask_bootstrap import Bootstrap
### from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, patch_request_class, UploadSet
from .configuration import configuration


def app_errorhandler(
        exception):
    response = jsonify({
            "status_code": exception.code,
            "message": exception.description,
        })
    return response, exception.code


uploaded_plans = UploadSet(
    name="plan",
    extensions=("png", "tif")
)
### db = SQLAlchemy()


def create_app(
        configuration_name):
    app = Flask(__name__)
    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)


    @app.errorhandler(400)
    def bad_request(exception):
        return app_errorhandler(exception)


    @app.errorhandler(404)
    def not_found(exception):
        return app_errorhandler(exception)


    @app.errorhandler(405)
    def method_not_allowed(exception):
        return app_errorhandler(exception)


    @app.errorhandler(422)
    def unprocessable_entity(exception):
        return app_errorhandler(exception)


    @app.errorhandler(500)
    def internal_server_error(exception):
        return app_errorhandler(exception)


    Bootstrap(app)

    configure_uploads(app, (uploaded_plans, ))
    patch_request_class(app, 32 * 1024 * 1024)  # <= 32 MiB

    ### db.init_app(app)


    # Attach routes and custom error pages.
    ### from .admin import admin as admin_blueprint
    ### app.register_blueprint(admin_blueprint)

    from .api import api_blueprint
    app.register_blueprint(api_blueprint)

    ### from .auth import auth as auth_blueprint
    ### app.register_blueprint(auth_blueprint)

    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")

    ### from .main import main as main_blueprint
    ### app.register_blueprint(main_blueprint)


    def format_pathname_(
            string,
            max_length):
        assert max_length > 3
        if len(string) > max_length:
            string = "...{}".format(string[-(max_length-3):])
        return string

    @app.template_filter()
    def format_pathname(
            string):
        return format_pathname_(string, 50)


    ### with app.app_context():
    ###     # http://stackoverflow.com/questions/19437883/when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w
    ###     # Extensions like Flask-SQLAlchemy now know what the "current" app
    ###     # is while within this block.
    ###     db.create_all()


    return app









### from flask import Flask, jsonify, request
### from flask.json import dumps
### import pika
### 
### 
### app = Flask(__name__)
### app.config.from_object("nc_assessment.default_settings")
### 
### 
### @app.route("/ping")
### def ping():
###     return jsonify(response="pong"), 200
### 
### 
### @app.route("/register_plan",
###         methods=["POST"])
### def register_plan():
###     """
###     Register a land-use plan with the geodatabase
### 
###     This call is asynchronous. Sometime in the future, the plan will be
###     registered. If so, a WMC end-point will be available for it, so you
###     can visualize it.
###     """
###     data = request.get_json()
###     id = data["id"]
###     name = data["name"]
###     app.logger.debug(dumps({
###         "nc_route": "register_plan",
###         "nc_id": id,
###         "nc_name": name
###     }))
### 
###     # Add a message to the message broker asking for the registration of
###     # the plan.
### 
###     queue_name = "register_plan"
###     message = dumps({
###         "id": id,
###         "name": name
###     })
### 
###     connection = pika.BlockingConnection(pika.ConnectionParameters(
###         host="rabbitmq"))
###     channel = connection.channel()
### 
###     channel.queue_declare(queue=queue_name, durable=True)
### 
###     channel.basic_publish(
###         exchange="",
###         routing_key=queue_name,
###         body=message,
###         properties=pika.BasicProperties(
###             delivery_mode = 2, # make message persistent
###         )
###     )
###     connection.close()
### 
###     return jsonify({
###         "_links": {
###             "wms_plan": {
###                 "href": "wms_plan"
###             }
###         }
###     }), 201
### 
### 
### @app.route("/wms_plan",
###         methods=["GET"])
### def wms_plan():
###     """
###     Ask for WMS end point for the plan uploaded during session with the id
###     passed in
### 
###     This call is synchronous. It will wait until the WMS end-point
###     is available, or the timeout has passed.
###     """
###     data = request.get_json()
###     id = data["id"]
### 
###     return jsonify({
###         "link": "blah"
###     }), 200
