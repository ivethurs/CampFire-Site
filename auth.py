from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json
import base64

# creating the auth blueprint
auth = Blueprint('auth', __name__)

# creating the login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if user want to login 
    if request.method == "POST":
        email = request.form.get("email") # getting the email information from the form 
        password = request.form.get("password") # getting the password information from the form
        
        user = User.query.filter_by(email=email).first() # getting the user by email
        if user:
            # check if the user password is correct
            # here in this if statement we have check_password_hash function
            # this function convert the user password to the hash password and then compare 
            # if password is match then logged in successfully message will show
            if check_password_hash(user.password, password): 
                flash("Logged in successfully!!", category="success")
                login_user(user, remember=True) # set login user to true
                return redirect(url_for("views.home")) # redirect to the home page
            else:
                flash("Incorrect password, try again", category="error") # if password is incorrect 
        else:
            flash("Email does not exists.", category="error") # flash message if email doesnot exists

    # render the template to login.html
    return render_template("login.html", user=current_user)

# router to logout the user
@auth.route('/logout') 
@login_required # you need login
def logout():
    # flask function to logout user
    logout_user()
    # redirect to login page
    return redirect(url_for('auth.login'))


# router to signup the user
@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        firstName = request.form.get("firstName") # getting the first name from the form 
        lastName = request.form.get("lastName") # gettng the last name from the form 
        email = request.form.get("email") # getting the email from the form 
        password = request.form.get("password") # getting the password from the form 
        confirmPassword = request.form.get("confirmPassword") # getting the confirm password from the form 
        file = request.files['profile-image'] # getting the image from the form 
        user = User.query.filter_by(email=email).first() # getting the user by email id form database
        
        # user already exists then show email already exists 
        if user:
            flash("Email already exists")
        elif len(firstName) < 2:
            flash("First name must be greater than 1 characters.", category="error") # if first name is not provided by user than flash message
        elif password != confirmPassword:
            flash("Password don't match.", category="error") # if password and confirm password doesnot match then flash message
        elif len(password) < 7:
            flash("Password must be at least 7 characters.", category="error") # password should alteast 7 character long
        else:
            followings = json.dumps([]) # creating an followings list and convert it into the string 
            followers = json.dumps([]) # creating a follower list and convert it into the string
            base64_image = base64.b64encode(file.read()).decode("utf-8") # convert image to base 64
            # creating a new user
            new_user = User(first_name=firstName, last_name=lastName, email=email, password=generate_password_hash(password, method="sha256"), followers=followers, followings=followings, profile=base64_image)
            db.session.add(new_user) # adding new user to database
            db.session.commit() # save changes to database
            flash("Account created", category="success") # flash message that you account is created 
            return redirect(url_for("views.home")) # redirect to home apge 

    # render signup page    
    return render_template("signup.html", user=current_user)