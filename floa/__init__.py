
from flask import Flask
from floa.models.catalog import Catalog
from floa.models.library import Library

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
    catalog = Catalog(app=app)

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
