# -*- coding: utf-8 -*-
import os

from flask import Flask, send_from_directory
from flask_graphql import GraphQLView

from demo.config import config
from demo.extensions import db, migrate
from demo.gql import schema

CLIENT_APP_DIR = "client/build"


def create_app(config_name='default'):
    """Create Flask application."""
    app = Flask(__name__, static_folder=CLIENT_APP_DIR)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_extensions(app)
    
    from demo.blueprints import main
    app.register_blueprint(main.main_bp)

    @app.route("/", defaults={"path": ""})
    @app.route("/<string:path>")
    @app.route("/<path:path>")
    def catch_all(path):
        filename = "index.html"
        if os.path.isfile(os.path.join(CLIENT_APP_DIR, path)):
            filename = path
        return send_from_directory(CLIENT_APP_DIR, filename)

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=app.config["DEBUG"]),
    )
    
    return app


def register_extensions(app):
    """Register extensions
    """
    db.init_app(app)
    migrate.init_app(app, db)
