from flask import Flask
import os


def create_app():
    app = Flask(
        __name__,
        template_folder="templates"
    )
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.config.from_pyfile('config.py')

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    from floa.extensions import db
    db.init_db(app)

    return app


if __name__ == "__main__":
    create_app().run()
