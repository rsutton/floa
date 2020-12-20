import datetime as dt
from flask import Blueprint, render_template, request, current_app as app
from floa.models.library import Library

bp = Blueprint(
    'home',
    'errors',
    'routes',
    url_prefix="/"
)

@app.errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404

@app.errorhandler(500)
def handle_500(err):
    return render_template('500.html'), 500

library = Library(ctx=app)

@app.context_processor
def context_process():
    last_update = library.load().last_update
    catalog_count = len(library.catalog)
    return dict(last_update=last_update, catalog_count=catalog_count)

@bp.route("/")
def home():
    library.load()
    return render_template('home.html', data=dict(library = library.library, catalog = library.catalog))

@bp.route("/_update/item", methods=["POST"])
def update_book_status():
    library.set_status(
        id=request.json['id'], 
        status=request.json['status']
    )
    return "OK"
