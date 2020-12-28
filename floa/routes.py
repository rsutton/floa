from datetime import datetime as dt
from flask import Blueprint, render_template, request, current_app as app
from flask_login import current_user
from floa.extensions import loa


bp = Blueprint(
    name='home',
    import_name=__name__,
    url_prefix="/"
)


@app.errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404


@app.errorhandler(500)
def handle_500(err):
    return render_template('500.html'), 500


@app.context_processor
def context_process():
    last_update = loa.last_update
    catalog_count = len(loa.catalog)
    return dict(last_update=last_update, catalog_count=catalog_count)


@bp.route("/")
def home():
    loa.check_for_updates()
    return render_template(
            'home.html',
            data=dict(catalog=loa.catalog)
        )

@bp.route("/_update/item", methods=["POST"])
def update_book_status():
    if current_user.is_authenticated:
        current_user.library.set_status(
            id=request.json['id'],
            status=request.json['status']
        )
        current_user.save()
    return "OK"
