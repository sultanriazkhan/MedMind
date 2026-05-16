from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        if not email or not password:
            flash("Email and password are required.", "error")
            return redirect(url_for("auth.login"))

        user = User.get_by_email(email)

        if user:
            login_user(user, remember=remember)

            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)

            return redirect(url_for("dashboard.dashboard_home"))

        flash("Invalid login credentials.", "error")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("auth.signup"))

        user = User(
            id="1",
            email=email,
            name=name
        )

        login_user(user)
        return redirect(url_for("home.landing"))

    return render_template("auth/signup.html")


@auth_bp.route("/forgot-password")
def forgot_password():
    return render_template("auth/forgot_password.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))