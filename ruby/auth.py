"""This file defines the blueprint that will handle all of the authentication views"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ruby.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')  # this is the Blueprint object that will handle requests


# Now we create the "Register" view - for registering a new user
# This is handled at '/auth/register' so auth is the Blueprint and register is a view within the Blueprint
@bp.route('/register', methods=('GET', 'POST'))  # note that the route is now from the blueprint not app
def register():
    if request.method == 'POST':  # i.e. if the user is submitting the register user form
        username = request.form['username']  # request.form is a dictionary mapping
        password = request.form['password']
        db = get_db()  # retrieve the database connection to sqlite
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # note that db.execute will escape characters so no risk of SQL injection attacks in flask
                # INSERT INTO <table> (col_name1, col_name2, ..) VALUES (value1, value2)
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",  # insert into table ? = placeholder
                    (username, generate_password_hash(password)),  # replace the ? in the query
                )
                db.commit()  # we have made a change to a table so we need to commit those changes
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))  # url_for login page and then redirect to it

        flash(error)

    return render_template('auth/register.html')  # render_template will render the HTML and display the
    # registration form written there.


# And now the view for the login given a username and password
@bp.route('/login', methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()

        error = None
        user = db.execute("SELECT * FROM user WHERE username = ?",
                          (username,)
                          ).fetchone()  # get the row from the user table with correct username

        if user is None:
            error = 'No such username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password for user'  # check that stored password matches the one entered

        if error is None:
            session.clear()  # session is a dictionary that can be accessed across requests
            # that data is stored in a *cookie*
            session['user_id'] = user['id']  # so we store the user id from the user table
            return redirect(url_for('index'))  # take user back to the homepage id logged in successfully

        flash(error)

    return render_template('auth/login.html')


# This is run before any view in the Blueprint and can check if we have stored session data
# for the user
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# Remember to log the user out by clearing the cache (data stored in session)
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Returns a view if there is a user_id attached to the session
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


