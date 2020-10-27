from flask import Blueprint
from flask import (
    render_template,
    request
)

from ..controller.registery import Registery

registery_router = Blueprint(
    "registery",
    __name__)

controller = Registery()

@registery_router.route("/registery/register", methods=["GET", "POST"])
def register():

    if controller.form_is_empty(request):
        return render_template('page.html')

    return controller.register_user(request)