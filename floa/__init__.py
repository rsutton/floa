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

    current = library.catalog
    latest = LoA().get_latest()
    library.last_update = dt.datetime.now().strftime('%d-%b-%Y %H:%M:%S')

    diff = library.compare(latest, current)
    if len(diff) > 0:
        # latest is authoritative so overwrite the catalog
        library.catalog = latest
        # add new items to library
        library.add(latest)

    library.save().load()
