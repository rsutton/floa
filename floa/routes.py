from flask import Blueprint, render_template, jsonify, request
from flask import current_app as app
import os.path
from floa.models.library import Library
from floa.models.catalog import Catalog

bp = Blueprint(
    'home',
    'routes',
    url_prefix="/"
)

# globals
library_file = os.path.join(os.path.dirname(app.instance_path), app.config['LIBRARY_FILENAME'])
library = Library(fname=library_file)
library.load()

catalog_file = os.path.join(os.path.dirname(app.instance_path), app.config['CATALOG_FILENAME'])
loa_url = app.config['LOA_COLLECTION_URL']
catalog = Catalog(fname=catalog_file, url=loa_url)
catalog.load()

@bp.route("/")
def home():
    return render_template('home.html', list=library.library)

@bp.route("/_update/item", methods=["POST"])
def update_book_status():
    result = library.set_book_status(
                id=request.json['id'], 
                status=request.json['status']
            )
    library.save()
    return result

@bp.route("/_update/catalog")
def update_catalog():
    latest = catalog.get_latest()
    diff = catalog.compare(latest, catalog.catalog)
    if len(diff) > 0:
        # latest is authoritative so overwrite the catalog
        catalog.catalog = latest
        catalog.save()
        # add new items to library
        library.add(diff)
    return jsonify(diff)
