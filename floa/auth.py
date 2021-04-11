from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for)
from flask_login import login_user
from flask_login.utils import login_required, logout_user
from oauthlib.oauth2.rfc6749.clients.base import AUTH_HEADER
from floa.models.user import User
from floa.extensions import loa, client
from instance.config import (
    AUTH_ENABLED,
    GOOGLE_DISCOVERY_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET)
import requests
import json


bp = Blueprint(
    name='auth',
    import_name=__name__,
    url_prefix="/"
)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@bp.route('/login')
def login():
    if AUTH_ENABLED:
        # Find out what URL to hit for Google login
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)
    else:
        return render_template('login.html')

@bp.route('/login_post', methods=['POST'])
def login_post():
    # use when AUTH_ENABLED = False else login_callback
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
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Doesn't exist? Add it to the database.
    # if not User.get(unique_id):
    #     user = User(unique_id, users_name, users_email)

    # Begin user session by logging the user in
    # replace with lookup from Google oauth response
    user = User.get_by_email(users_email)
    if not user:
        # flash something here
        return redirect(url_for('auth.login'))

    login_user(user, remember=True)
    # update user's library with latest catalog
    user.library.update(loa.catalog)
    return redirect(url_for('home.home'))


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