from quart import Quart, render_template
from .routes.registery import registery_router
from ..orm.engine import migrate

def create_app():

    app = Quart(__name__, template_folder="templates", static_folder="static")

    app.register_blueprint(registery_router, url_prefix="/registery")

    @app.errorhandler(404)
    async def page_not_found(*args):
        return await render_template("home.html")

    app.debug = True
    return app


if __name__ == "__main__":
    migrate()
    app = create_app()
    app.run()