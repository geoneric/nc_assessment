from flask import Blueprint


api_blueprint = Blueprint("api", __name__)


from . import api, assessment_request, lu_classes, ping, plan, user
