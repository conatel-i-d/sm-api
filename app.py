import os

from app import create_app
from alembic.config import Config
from alembic import command

FLASK_ENV = os.environ.get('FLASK_ENV', 'test')
FLASK_PORT = os.environ.get('FLASK_PORT', 5000)

alembic_cfg = Config("./alembic.ini")
alembic_cfg.set_main_option('sqlalchemy.url', os.environ['DATABASE_URI'])

(app, _) = create_app(FLASK_ENV)

if __name__ == "__main__":
    command.upgrade(alembic_cfg, "head")
    app.run(host='0.0.0.0', port=FLASK_PORT)