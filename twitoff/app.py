from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet


# Create own app factory
def create_app():
    # Create server
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')

    # Stop tracking modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['ENV'] = config('ENV')

    # Now the database knows about the app
    DB.init_app(app)

    # Create the route
    @app.route("/")
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    return app