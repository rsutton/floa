import datetime as dt
from flask import Flask
from floa.models.catalog import Catalog
from floa.models.library import Library
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
    library = Library(app=app)
    if os.path.exists(library.filename):
        library.load()

    catalog = Catalog(app=app)
    if os.path.exists(catalog.filename):
        catalog.load()
    current = catalog.catalog

    latest = catalog.get_latest()
    diff = catalog.compare(latest, current)
    if len(diff) > 0:
        # latest is authoritative so overwrite the catalog
        catalog.catalog = latest
        catalog.save()
        catalog.last_update = dt.datetime.now()
        # add new items to library
        library.add(latest)
    library.load()
