from flask import jsonify
from . import api_blueprint


@api_blueprint.route("/api")
def api():
    return jsonify({
        "resources": {
            "plans": {
                "route": "/plans"
            },
            "lu_classes": {
                "route": "/lu_classes"
            }
        }
    }), 200
