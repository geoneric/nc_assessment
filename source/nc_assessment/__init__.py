from flask import Flask


app = Flask(__name__)
app.config.from_object("nc_assessment.default_settings")


@app.route("/ping")
def ping():

    return "pong (nc_assessment)"
