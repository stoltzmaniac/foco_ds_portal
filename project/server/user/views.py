# project/server/user/views.py
import json

from flask import render_template, Blueprint, url_for, redirect, flash, request, g
from flask_login import login_user, logout_user, login_required

from project.server import bcrypt, db
from project.server.user.models import User
from project.server.user.forms import LoginForm, RegisterForm
from project.server.config import BaseConfig


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        user.save()
        # db.session.add(user)
        # db.session.commit()

        login_user(user)

        flash("Thank you for registering.", "success")
        return redirect(url_for("user.members"))

    return render_template("user/register.html", form=form)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            flash("You are logged in. Welcome!", "success")
            return redirect(url_for("user.members"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("user/login.html", form=form)
    return render_template("user/login.html", title="Please Login", form=form)


@user_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out. Bye!", "success")
    return redirect(url_for("main.home"))


@user_blueprint.route("/members")
@login_required
def members():
    with open('./jupyter_tokens/nbserver-1.json') as json_file:
        data = json.load(json_file)
        jupyter_token = data['token']
        jupyterlab_domain = f"{BaseConfig.WEB_DOMAIN}:8888/?token={jupyter_token}"
        jupyterhub_domain = f"{BaseConfig.WEB_DOMAIN}:8888"
    return render_template("user/members.html",
                           jupyterlab_domain=jupyterlab_domain, jupyterhub_domain=jupyterhub_domain)
