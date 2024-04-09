from flask import Blueprint, request

import controllers

auth = Blueprint('auth', __name__)


@auth.route("/auth/user", methods=["POST"])
def auth_token_add():
    return controllers.auth_token_add(request)
