from flask import Blueprint, render_template, request, current_app as app
from floa.extensions import loa
from floa.models.library import Library
from floa.models.user import User


bp = Blueprint(
    'home',
    'errors',
    'routes',
    url_prefix="/"
)

catalog = loa.get_loa()

try: 
    library = User.get(0).library
except AttributeError as ae:
    print(f'User does not exist: {ae}')
    library = Library()

@app.errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404


@app.errorhandler(500)
def handle_500(err):
    return render_template('500.html'), 500


@app.context_processor
def context_process():
    last_update = loa.last_update
    catalog_count = len(catalog)
    return dict(last_update=last_update, catalog_count=catalog_count)


@bp.route("/")
def home():
    return render_template(
            'home.html',
            data=dict(library=library.library, catalog=catalog)
        )


@bp.route("/_update/item", methods=["POST"])
def update_book_status():
    library.set_status(
        id=request.json['id'],
        status=request.json['status']
    )
    return "OK"
