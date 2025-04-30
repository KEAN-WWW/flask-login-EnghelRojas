from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from application.database.models import User

authentication = Blueprint("authentication", __name__)

@authentication.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        from application import db  # avoid circular import
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("User Not Found")
            return redirect(url_for("authentication.login"))

        if not check_password_hash(user.password, password):
            flash("Password Incorrect")
            return redirect(url_for("authentication.login"))

        login_user(user)
        return redirect(url_for("authentication.dashboard"))

    return render_template("login.html")

@authentication.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@authentication.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("authentication.login"))
