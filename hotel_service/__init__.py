# init.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 


# This is mainly for creating an absolute path to the running file
# with the inline 'if-else' exception incase it's imported from the pyshell.
app_root = os.path.dirname(os.path.abspath('.' if not '__file__' in locals() else __file__))
template_folder = os.path.join(app_root, 'templates')

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# Create an instance of the Flask class
# Assigning the 'static' url path since we'll need files that we stored in the 'static/' folder
#    like our images 'static/images', and from the url should be accessible
#    from 'http://localhost:5000/static/<file-path>'
# Set the absolute path for the templates, to prevent unwanted os related pathname issues.
app = Flask(__name__)

# App configs
# 'SECRET_KEY', is used for user authentication. It REALLY shouldn't be hardcoded irl, but lets let it slide.
# 'SQLALCHEMY_TRACK_MODIFICATIONS' => true, just suppresses some unwanted warnings from sqlalchemy
# 'SQLALCHEMY_DATABASE_URI' => <uri-path>, sets the db uri to read/write to a local db file './db.sqlite'
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

# Setup an instance of the Flask-Login's LoginManager
# and assign the login_views name to the name of our login 
# route.
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Add the table schema's for the user accounts and hotel 
# rooms.
from .models import Account, HotelRoom

# Create tables to database
# A fix to a 'RuntimeError' when trying to write to the database from outside the 
# application context.
# https://flask.palletsprojects.com/en/2.0.x/appcontext/#manually-push-a-context
with app.app_context():
    db.create_all(app=app)

app.app_context().push()


# Add a user loader callback for reloading the user object 
# from the user ID stored in the session.
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Account.query.get(int(user_id))

# Blueprints for our authentication routes for our app.
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# Blueprints for the the main data handling 
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

# Just the function to not have to run within the Flask agent
# and having to use commands.
app.run(
    host='127.0.0.1',
    port=5000
)