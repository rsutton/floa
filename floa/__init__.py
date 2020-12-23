from flask import Flask
from floa.models.library import Library
from floa.models.loa import LoA
import datetime as dt
import os.path

def create_app():
    app = Flask(
        __name__,
        template_folder="templates"
    )
    app.config.from_pyfile('config.py')

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)
        init_app(app)
    return app

def init_app(app):
    library = Library(ctx=app)
    if os.path.exists(library.filename):
        library.load()
    latest = LoA.get_latest()
    library.update(latest)
