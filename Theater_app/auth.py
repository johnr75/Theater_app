from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from Theater_app import mongo
from .forms import LoginForm
auth = Blueprint('auth', __name__)


@auth.route("/login.html", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        users = mongo.db.Users
        login_user = users.find_one({'username': request.form['username']})
        if login_user:
            if login_user['password'] == request.form['password']:
                session['username'] = request.form['username']
                session['access'] = login_user['access']
                return redirect(url_for('main.welcome'))
        flash("Login Failed! Please try again")
        return render_template("login.html", form=form)

    else:
        return render_template("login.html", form=form)