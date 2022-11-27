from flask import render_template, request, redirect, url_for, flash, Blueprint
from .extensions import mongo, login_manger
from .forms import LoginForm, ChangePassword
from .auth import *
from flask_login import login_required, logout_user, fresh_login_required, current_user


auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        suc = user_login(mongo.db.Users, request.form['username'], request.form['password'])
        if suc:

            return redirect(url_for('main.welcome'))
        else:
            flash("Login Failed! Please try again")
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)


@auth.route("/profile", methods=['GET', 'POST'])
@login_required
@fresh_login_required
def profile():
    form = ChangePassword()

    if form.validate_on_submit():
        suc = change_password(mongo.db.Users, request.form['password'], current_user.member_data['username'])
        if suc:
            flash('Password has been updated')
            return redirect(url_for('main.welcome'))
        flash('Password NOT updated')
        return render_template("update_profile.html", form=form)
    else:
        for error in form.password.errors:
            flash(error)
        return render_template("update_profile.html", form=form)
    return render_template("update_profile.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    edit_items = ({'session_token': ""})
    mongo.db.Users.update_one({'session_token': current_user.member_data['session_token']}, {"$set": edit_items},
                              upsert=False)
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('auth.login'))


@auth.route('/create')
def create():
    username = 'Jay'
    password = '1234'
    st = create_user(mongo.db.Users, username, password)
    if st:
        return f'<h1>New user {username} has been created!</h1>'
    return f'<h1>New user {username} was not created!</h1>'
