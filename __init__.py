from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# initialize the database
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__) # initializing flask app
    app.config['SECRET_KEY'] = 'the secret key' # assigning the secret key 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # getting the database string 
    db.init_app(app) # telling flask app that we are using SQLAlchemy as a database

    # importing the data from another file
    from .views import views
    from .auth import auth

    # registering the blueprint
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")

    from .models import User
    create_database(app) # calling create database to create empty tables into the database

    # initialze the logingManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app) # creating connection between login manager and the flask app

    # loading up the user 
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # return the flask app
    return app

# creating the database
def create_database(app):
    # if tables not exists in database then create it 
    if not path.exists("website/"+DB_NAME):
        db.create_all(app=app)
        print("created database")
