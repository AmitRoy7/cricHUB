from flask import redirect, session, render_template, Blueprint

from cricMongoDB.database import db

app = Blueprint('profile', __name__)


class Facade:

    def __init__(self=None):
        return


class Subsystem1:

    @app.route('/profile/')
    def profile(self=None):
        if 'username' not in session.keys():
            return redirect('/auth/signin')

        users = db.users

        loogged_in = session["username"]
        query = {"username": loogged_in}

        profile = users.find_one(query)

        return render_template('profile/profile.html', name=profile["name"], email=profile["email"], phone=profile["phone_number"])
