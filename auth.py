from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db
from flask_login import login_user, login_required, logout_user, current_user

#this file is a blueprint of our application, has a bunch of urls defined in it
auth = Blueprint('auth', __name__)

#setting up the routes (part of Flask)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') # get the email from the form
        password = request.form.get('password') # get the password from the login form

        #what do you when you are looking for a specific entry in your database
        user = User.query.filter_by(email=email).first() #returns the first result, bc each user must have a unique email anyway
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember = True) #the user we found with the correct email and password is the one we are logging in here
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", boolean = True)
        

@auth.route('/logout')
@login_required #we cannot access this route unless the user is logged in
def logout():
    logout_user() #no need to pass a user, it will just logout the current user
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #need to check if the username that the user signs up with is already taken or not (because usernames must be unique)
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category = 'error')
        #start by making sure this info is valid
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category = 'error') #flashes a message on screen
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category = 'error')
        elif password1 != password2:
            flash('Passwords don\'t', category = 'error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category = 'error')
        else:
            #create a new user
            new_user = User(email=email, first_name = first_name, password = generate_password_hash(password1, method = 'sha256')) #sha256 is a hashing algorithm
            #add the account to the database
            db.session.add(new_user)
            #need to make a commit to the database (means we made a change to the database and now we must commit it)
            db.session.commit()
            login_user(user, remember = True)
            # add user to the database
            flash('Account created!', category = 'success')
            #return a redirect for the home page
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")