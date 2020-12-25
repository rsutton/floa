from flask import Blueprint, render_template, request, current_app as app
from flask_login import current_user
from floa.extensions import loa


bp = Blueprint(
    name='home',
    import_name=__name__,
    url_prefix="/"
)

catalog = loa.get_loa()

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
    if current_user.is_authenticated:
        return render_template(
                'home.html',
                data=dict(library=current_user.library, catalog=catalog)
            )
    else:
        return '<a class="button" href="/login">Google Login</a>'

@bp.route("/_update/item", methods=["POST"])
def update_book_status():
    if current_user.is_authenticated:
        current_user.library.set_status(
            id=request.json['id'],
            status=request.json['status']
        )
        return "OK"
    else:
        return '<a class="button" href="/login">Google Login</a>'
