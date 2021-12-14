from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# this is a user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # id of the user
    first_name = db.Column(db.String(150)) # first name of the user
    last_name = db.Column(db.String(150)) # last name of the user
    email = db.Column(db.String(150), unique=True) # email id of the user
    password = db.Column(db.String(150))  # password of the user
    followers = db.Column(db.String(10000)) # followers of the user
    followings = db.Column(db.String(10000)) # followings of the user
    profile = db.Column(db.String(100000)) # profile of the user
    posts = db.relationship("Post") # maintian the relationship between post and user 
    

# post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id of the post
    data = db.Column(db.String(10000)) # message of the post
    likes = db.Column(db.String(10000)) # like on the post
    image = db.Column(db.String(100000)) # image of the post 
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # date of the post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # creating parent child relationship with user model
    user = db.relationship("User", backref="users") # create back reference to user