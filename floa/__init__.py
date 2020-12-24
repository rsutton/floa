from instance.config import SECRET_KEY
from flask import Flask
from floa.extensions import db

def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="templates"
    )
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    with app.app_context():
        # must put extensions before register_blueprint
        # because it doesn't return here
        db.init_db(app)

        from . import routes
        app.register_blueprint(routes.bp)

    return app
