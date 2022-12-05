from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config["DB_LOCAL"] = False
app.config["HOME_LOCATION"] = (33.5186,-86.8104)    #Birmingham, AL
app.config["DB_REMOTE_URI"] = "postgresql://Team6:team6@138.26.48.83:5432/Team6DB"
app.config["DB_LOCAL_URI"] = "postgresql://postgres:postgrespw@localhost:55000/postgres"
app.config['data'] = {}


# this import has to come after app because routes requires it
from web_site import routes_home
from web_site.backend import api






