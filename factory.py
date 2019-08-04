from flask import Flask
from extensions import db, bootstrap
from views import bp


def create_app(config=None):
    app = Flask(__name__)
    app.config.update({
        'PY2NEO_HOST': 'db',
        'PY2NEO_USER': 'neo4j',
        'PY2NEO_PASSWORD': 'Gale123#'
    })
    app.config.update(config or {})

    db.init_app(app)
    bootstrap.init_app(app)

    app.register_blueprint(bp)

    return app
