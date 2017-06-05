from flask import Blueprint


api_blueprint = Blueprint("api", __name__)


from . import api, lu_classes, ping, plan, user
