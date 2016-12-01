import os
### import tempfile


class Configuration:

    # Flask
    SECRET_KEY = os.environ.get("NC_SECRET_KEY") or "yabbadabbadoo!"
    JSON_AS_ASCII = False

    BOOTSTRAP_SERVE_LOCAL = True

    ### SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ### SQLALCHEMY_TRACK_MODIFICATIONS = False

    ### AGGREGATE_METHOD_HOST = "aggregate_method"
    ### AGGREGATE_QUERY_HOST = "aggregate_query"


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

    ### AGGREGATE_METHOD_PORT = 5000
    ### AGGREGATE_QUERY_PORT = 5000


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        from flask_debug import Debug
        Debug(app)


class TestingConfiguration(Configuration):

    TESTING = True

    ### SQLALCHEMY_DATABASE_URI = os.environ.get("NC_TEST_DATABASE_URI") or \
    ###     "sqlite:///" + os.path.join(tempfile.gettempdir(), "assessment-test.sqlite")

    ### AGGREGATE_METHOD_PORT = 5000
    ### AGGREGATE_QUERY_PORT = 5000


class ProductionConfiguration(Configuration):

    pass

    ### SQLALCHEMY_DATABASE_URI = os.environ.get("NC_DATABASE_URI") or \
    ###     "sqlite:///" + os.path.join(tempfile.gettempdir(), "assessment.sqlite")

    ### AGGREGATE_METHOD_PORT = 9090
    ### AGGREGATE_QUERY_PORT = 9090


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "production": ProductionConfiguration
}
