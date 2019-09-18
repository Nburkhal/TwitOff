from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()

# Create user class
class User(DB.Model):
    '''Instantiate user class'''
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Tweet(DB.Model):
    '''Instantiate tweet class'''
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280))
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet {}>'.format(self.text)