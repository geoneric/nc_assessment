from flask import jsonify
from . import api_blueprint


@api_blueprint.route("/api")
def api():
    return jsonify({
        "resources": {
            "lu_classes": {
                "route": "/lu_classes"
            },
            "plans": {
                "route": "/plans"
            },
            "users": {
                "route": "/users"
            },
        }
    }), 200
