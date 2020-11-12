from .app.app import create_app
from .bot.bot import bot
from .orm.engine import migrate
from . import config
import hypercorn

app = create_app()

if __name__ == "__main__":
    migrate()
    bot.loop.create_task(app.run_task('0.0.0.0'))
    bot.run(config.token)