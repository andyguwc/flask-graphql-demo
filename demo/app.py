# -*- coding: utf-8 -*-
from flask import Flask
from flask_graphql import GraphQLView

from demo.config import config
from demo.extensions import db, migrate
from demo.gql import schema


def create_app(config_name='default'):
    """Create Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_extensions(app)
    
    from demo.blueprints import main
    app.register_blueprint(main.main_bp)

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
