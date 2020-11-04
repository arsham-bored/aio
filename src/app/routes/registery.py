from quart import Blueprint
from quart import (
    render_template,
    request
)

from ..controller.registery import Registery

registery_router = Blueprint(
    "registery",
    __name__)

controller = Registery()

@registery_router.route("/register", methods=["GET", "POST"])
async def register():

    
    if request.method == "GET":
        return await render_template('page.html')

    return await controller.register_user(request)

@registery_router.route("/register/succes")
async def success():
    return await render_template("ok.html")

@registery_router.route("/register/fail")
async def fail():
    return await render_template("failed.html")