from flask import Blueprint, render_template, request, jsonify, flash, redirect
from flask.helpers import url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db
import json
import base64

# we are creating a view blueprint
# basically, a flask blueprint is a way to organize the file structure of application
views = Blueprint('views', __name__)

# defining a home page route 
@views.route('/', methods=['POST', 'GET'])
@login_required # In order to access the home page you have to create an account and login
def home():
    # if the user want to create a post
    if request.method == "POST":
        # get the post data from the form
        post = request.form.get("post")
        # get the post image from the form if it is available
        file = request.files['image']
        # if post size is short then flash a message
        if len(post) < 1:
            flash("Post is too short!", category="error")
        else:
            likes = [] # creating a like array
            serialized = json.dumps(likes) # converting that array to a string so that we can store it into database
            base64_image = base64.b64encode(file.read()).decode("utf-8") # convert image to base64
            # creating a new post 
            new_post = Post(data=post, likes=serialized, user_id=current_user.id, image=base64_image, user=current_user)
            # adding that post to the database
            db.session.add(new_post)
            # saving the data to the database
            db.session.commit()
            # flash the message that post is added to database
            flash("Post added!!")
    
    # get all the post from database
    posts = Post.query.all()
    # render the template with home.html file and user and post info
    return render_template("home.html", user=current_user, posts=posts)    

# creating the route to like and unlike the post
@views.route("/like_unlike_post", methods=['POST'])
@login_required # to like and unlike the post you have to login first
def likePost():
    post = json.loads(request.data)  # get the form data 
    postId = post['postId'] # get post id 
    post = Post.query.get(postId) # get the post by id
    likes = json.loads(post.likes) # get the post like and convert it into the list of array
    flag = True 
    # here is the logic if the user already liked the post than unlike it otherwise like that post
    for like in likes:
        if like == current_user.id:
            flag = False
            likes.remove(like)
            break

    # if user haven't like the post that append user id to post array
    if flag:
        likes.append(current_user.id)
        
    # update the like field in database
    post.likes = json.dumps(likes)
    # save changes to the database
    db.session.commit()
    # redirect to the home page
    return redirect(url_for("views.home"))

# get the current user profile
@views.route("/profile", methods=['GET'])
@login_required # to get profile you have to login first
def profile():
    # render the profile.html page to the user
    return render_template("profile.html", user=current_user)

# creating a route to get profile by user id
@views.route("/profile/<id>", methods=['GET'])
@login_required # you need to login 
def user_profile(id):
    # get the user data from database by his/her id
    user = User.query.get(id)
    # render the profile.html template 
    return render_template("profile.html", user=user, current_user=current_user)

# creating a route to follow a user
@views.route("/follow", methods=['POST'])
@login_required # you need to login
def follow():
    user = json.loads(request.data)    # getting the form data
    userId = user['userId'] # getting the id of user
    user = User.query.get(userId) # getting the user data from his/her id
    followings = json.loads(current_user.followings) # getting the followings of user and store it into the list
    followers = json.loads(user.followers) # getting the follower of user and store it into the list
    followers.append(current_user.id)
    followings.append(userId)  
    # updating the follower field of the user
    user.followers = json.dumps(followers) 
    # update the following field of the user
    current_user.followings = json.dumps(followings)
    # save field to database
    db.session.commit()
    # redirect to the home page
    return redirect(url_for("views.home"))

# route to unfollow the user
@views.route("/unfollow", methods=['POST'])
@login_required # you need to login first 
def unfollow():
    user = json.loads(request.data) # getting the form data
    userId = user['userId'] # getting the id of the user
    user = User.query.get(userId) # getting user data from his/her id
    followings = json.loads(current_user.followings) # getting the following of the user
    followers = json.loads(user.followers) # getting the follower of the user

    followers.remove(current_user.id) # remove the user id from the followers
    followings.remove(userId) # remove the user id from the folloing 

    user.followers = json.dumps(followers) # converting the list to string and store to the database
    current_user.followings = json.dumps(followings) # converting the list to string and store to the database
    db.session.commit() # save changes on the database

    # redirect to the home page
    return redirect(url_for("views.home"))

# getting follower by user id
@views.route('/followers/<id>', methods=['GET'])
@login_required # you need to login 
def followers(id):
    # getting the user by id
    user = User.query.get(id)
    followers = json.loads(user.followers) # get the followers
    list = []
    # here we are iterating the follower and getting the data from the database
    # getting the user data by his/her id and store it into the list 
    for follower in followers:
        user = User.query.get(follower)
        list.append(user)
    # render the template 
    return render_template("followers.html", user=current_user, followers = list)

# getting the following information with user id
@views.route('/followings/<id>', methods=['GET'])
@login_required # you need login 
def followings(id):
    # getting the user by id 
    user = User.query.get(id)
    followings = json.loads(user.followings) # getting the followings list 
    list = []
    # iterating over the following list and getting the user information and store it into the list
    for following in followings:
        user = User.query.get(following)
        list.append(user)
    # render followings.html template
    return render_template("followings.html", user=current_user, followings = list)
    

# router to delete the post
@views.route('/deletePost', methods=['POST'])
@login_required # you need to login 
def delete_post():
    post = json.loads(request.data) # getting the form data
    postId = post['postId'] # getting the post id from the form
    post = Post.query.get(postId) # getting the post by id 

    if post:
        if post.user_id == current_user.id:
            # getting the post and delete it 
            db.session.delete(post)
            # saving the changes into the database
            db.session.commit()
    
    return jsonify({}) # returning empty json 