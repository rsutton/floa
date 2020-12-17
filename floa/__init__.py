
from flask import Flask
import os.path
from .models.library import Library
from .models.catalog import Catalog

library = Library()
catalog = Catalog()

def create_app():
    app = Flask(
        __name__,
        template_folder="templates"
    )
    app.config.from_pyfile('config.py')

    library.init_app(app)
    catalog.init_app(app)

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

        init_library(app)
    return app

def init_library(app):
    library.load()
    catalog.load()
    latest = catalog.get_latest()
    diff = catalog.compare(latest, catalog.catalog)
    if len(diff) > 0:
        # latest is authoritative so overwrite the catalog
        catalog.catalog = latest
        catalog.save()
        # add new items to library
        library.add(diff)
    

