from quart import Quart
from .routes.registery import registery_router
from ..orm.engine import migrate

def create_app():

    app = Quart(__name__, template_folder="templates", static_folder="static")

    app.register_blueprint(registery_router, url_prefix="/registery")

    app.debug = True
    return app


if __name__ == "__main__":
    migrate()
    app = create_app()
    app.run()