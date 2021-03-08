from floa.models.loa import LoA
from floa.models.db import Database
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
from instance.config import GOOGLE_CLIENT_ID


loa = LoA()
db = Database()
login_manager = LoginManager()
# Setup oauth2 here
# https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html
client = WebApplicationClient(GOOGLE_CLIENT_ID)
