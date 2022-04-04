from flask import Blueprint, render_template
from flask_login import login_required, current_user

#this file is a blueprint of our application, has a bunch of urls defined in it
views = Blueprint('views', __name__)

@views.route('/') #for the home page
@login_required
def home():
    return render_template("home.html")