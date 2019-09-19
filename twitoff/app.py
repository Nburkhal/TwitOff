from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .predict import predict_user
from .twitter import add_update_user, update_all_users


# Create own app factory
def create_app():
    # Create server
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')

    # Stop tracking modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Now the database knows about the app
    DB.init_app(app)

    # Create the route
    @app.route("/")
    def root():
        users = User.query.all()
        if not users:
            DB.create_all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset database!')

    @app.route('/update')
    def update():
        update_all_users()
        return render_template('base.html', title='Update all users!', users=User.query.all())

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else:
            tweet_text = request.values['tweet_text']
            confidence = int(predict_user(user1, user2, tweet_text) * 100)
            if confidence >= 50:
                message = f'"{tweet_text}" is more likely to be said by {user1} than {user2}, with {confidence}% confidence'
            else:
                message = f'"{tweet_text}" is more likely to be said by {user2} than {user1}, with {100-confidence}% confidence'
        return render_template('prediction.html', title='Prediction', message=message)

    return app