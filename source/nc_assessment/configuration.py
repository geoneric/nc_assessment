import os
import tempfile


class Configuration:

    # Flask
    SECRET_KEY = os.environ.get("NC_ASSESSMENT_SECRET_KEY") or \
        "yabbadabbadoo!"
    JSON_AS_ASCII = False

    BOOTSTRAP_SERVE_LOCAL = True

    ### SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ### SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADS_DEFAULT_DEST = \
        os.environ.get("NC_UPLOADS_DEFAULT_DEST") or \
        tempfile.gettempdir()

    # NC_ASSESSMENT_HOST = "nc_assessment"
    NC_PLAN_HOST = "nc_plan"

    NC_RABBITMQ_DEFAULT_USER = os.environ.get("NC_RABBITMQ_DEFAULT_USER")
    NC_RABBITMQ_DEFAULT_PASS = os.environ.get("NC_RABBITMQ_DEFAULT_PASS")
    NC_RABBITMQ_DEFAULT_VHOST = os.environ.get("NC_RABBITMQ_DEFAULT_VHOST")


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    DEBUG = True
    DEBUG_TOOLBAR_ENABLED = True
    FLASK_DEBUG_DISABLE_STRICT = True

    ### SQLALCHEMY_DATABASE_URI = os.environ.get("NC_DEV_DATABASE_URI") or \
    ###     "sqlite:///" + os.path.join(tempfile.gettempdir(), "assessment-dev.sqlite")

    # NC_ASSESSMENT_PORT = 5000
    NC_PLAN_PORT = 5000


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        from flask_debug import Debug
        Debug(app)


class TestConfiguration(Configuration):

    # TESTING = True

    ### SQLALCHEMY_DATABASE_URI = os.environ.get("NC_TEST_DATABASE_URI") or \
    ###     "sqlite:///" + os.path.join(tempfile.gettempdir(), "assessment-test.sqlite")

    # NC_ASSESSMENT_PORT = 5000
    NC_PLAN_PORT = 5000


class ProductionConfiguration(Configuration):

    ### SQLALCHEMY_DATABASE_URI = os.environ.get("NC_DATABASE_URI") or \
    ###     "sqlite:///" + os.path.join(tempfile.gettempdir(), "assessment.sqlite")

    # NC_ASSESSMENT_PORT = 3031
    NC_PLAN_PORT = 3031


configuration = {
    "development": DevelopmentConfiguration,
    "test": TestConfiguration,
    "acceptance": ProductionConfiguration,
    "production": ProductionConfiguration
}
