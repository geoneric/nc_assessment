from flask import jsonify
from . import api_blueprint


@api_blueprint.route("/api")
def api():
    return jsonify({
        "resources": {
            "plans": {
                "route": "/plans"
            }
        }
    }), 200
