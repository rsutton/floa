from flask import Flask
import os


def create_app():
    app = Flask(
        __name__,
        template_folder="templates"
    )
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'data/database.data')
    )
    app.config.from_pyfile('config.py')

    try:
        os.makedirs(f'{app.instance_path}/data')
    except OSError:
        pass

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)
    return app
