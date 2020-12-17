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

@bp.route("/")
def home():
    with app.import_name('Library'):
        Library().load()
    return render_template('home.html', list=Library().library)

@bp.route("/_update/item", methods=["POST"])
def update_book_status():
    result = library.set_book_status(
                id=request.json['id'], 
                status=request.json['status']
            )
    return result


