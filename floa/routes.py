from flask import (
    Blueprint,
    render_template,
    request,
    session,
    current_app as app
    )
from flask_login import current_user
from floa.extensions import loa
from floa.models.library import Library


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
    return dict(
        last_update=last_update,
        catalog_count=catalog_count,
        session_library=session['LIBRARY'])


@bp.route("/")
def home():
    if current_user.is_authenticated:
        if loa.time_for_update():
            session['LIBRARY'] = Library(library=current_user.library.library)\
                .update(loa.catalog).library
        else:
            session['LIBRARY'] = current_user.library.library
    else:
        if 'LIBRARY' not in session:
            session['LIBRARY'] = Library().update(loa.catalog).library
    return render_template(
            'home.html',
            data=dict(catalog=loa.catalog)
        )

@bp.route("/_update/item", methods=["POST"])
def update_book_status():
    # create library list from the session object
    library = Library(library=session['LIBRARY'])
    library.set_status(
        id=request.json['id'],
        status=request.json['status']
    )
    # save updated library to session
    session['LIBRARY'] = library.library

    if current_user.is_authenticated:
        current_user.library = library
        current_user.save()
    return "OK"
