from flask import Flask
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
    library = Library(app)
    if os.path.exists(library.filename):
        library.load()

    current = library.catalog
    latest = library.get_latest()

    diff = library.compare(latest, current)
    if len(diff) > 0:
        # latest is authoritative so overwrite the catalog
        library.catalog = latest
        # add new items to library
        library.add(latest)

    library.save().load()
