from flask import Blueprint, render_template, request, current_app as app
from floa.models.catalog import Catalog
from floa.models.library import Library

bp = Blueprint(
    'home',
    'routes',
    url_prefix="/"
)

library = Library(app=app)

@bp.route("/")
def home():
    library.load()
    return render_template('home.html', list=library.library)

@bp.route("/_update/item", methods=["POST"])
def update_book_status():
    result = library.set_book_status(
                id=request.json['id'], 
                status=request.json['status']
            )
    return result


