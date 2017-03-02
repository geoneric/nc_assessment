from flask import jsonify
from . import api_blueprint


@api_blueprint.route("/lu_classes")
def lu_classes():
    return jsonify({
        "lu_classes": {
            "2": {
                "label": "water"
            },
            "3": {
                "label": "grass"
            },
            "4": {
                "label": "trees"
            },
            "5": {
                "label": "houses"
            }
        }
    }), 200
