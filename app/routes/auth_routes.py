from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for
)

import hashlib

from app import mysql

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )

        user = cur.fetchone()

        if user and user["password"] == hashed_password:

            session["username"] = username

            return redirect(
                url_for("trip.home_page")
            )

        else:

            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template(
        "login.html",
        error=None
    )


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        name = request.form["name"]

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )

        existing_user = cur.fetchone()

        if existing_user:

            return render_template(
                "signup.html",
                error="Username already exists"
            )

        cur.execute(
            """
            INSERT INTO users
            (username, password, name)
            VALUES (%s, %s, %s)
            """,
            (
                username,
                hashed_password,
                name
            )
        )

        mysql.connection.commit()

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "signup.html",
        error=None
    )


@auth_bp.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(
        url_for("trip.home_page")
    )