from flask import Blueprint, render_template, request, redirect, session, url_for
from flask_login import login_user
from flask_login.utils import login_required, logout_user
from floa.models.user import User
from floa.extensions import loa

bp = Blueprint(
    name='auth',
    import_name=__name__,
    url_prefix="/"
)


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/login_post', methods=['POST'])
def login_post():
    # replace with lookup from Google oauth response
    user = User.get_by_email(request.form.get('email'))
    if not user:
        # flash something here
        return redirect(url_for('auth.login'))
    login_user(user, remember=True)
    # update user's library with latest catalog
    user.library.update(loa.catalog)
    return redirect(url_for('home.home'))


@bp.route('/login/callback')
def login_callback():
    return 'Callback'


@bp.route('/logout')
@login_required
def logout():
    session.pop("LIBRARY", None)
    logout_user()
    return redirect(url_for('home.home'))

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')