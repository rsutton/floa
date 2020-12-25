from flask import Flask
from floa.extensions import db, login_manager

def create_app():
    ''' 
    The flask application factory function. Using environment variable
    FLASK_APP=module, specifying just an import path without an application name
    or factory function, then Flask will import your module or package and try
    to locate the application on its own. It will first look for an app or
    application global variable, and if neither is found it will inspect all
    global variables in the module looking for one that is set to an instance of
    class Flask. If none of these attempts produce an application, Flask will
    finally look for an application factory function in your module called
    either create_app() or make_app(). If Flask can’t still find your
    application, then the flask run command will exit with an error.
    '''
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="templates"
    )
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    with app.app_context():
        # must put extensions before register_blueprint
        # because it doesn't return here
        db.init_db(app)
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        from floa.models.user import User
        # Setup oauth2 here
        # https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html
        
        # Flask-Login helper to retrieve a user from our db
        @login_manager.user_loader
        def load_user(user_id):
            return User.get(user_id)


    with app.app_context():
        from . import routes, auth
        app.register_blueprint(routes.bp)
        app.register_blueprint(auth.bp)

    return app


if __name__ == "__main__":
    create_app().run()
