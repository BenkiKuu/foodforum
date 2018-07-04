from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(250), nullable=False)
    breakfast = db.relationship('Breakfast', backref='author', lazy=True)
    breakfastcomments = db.relationship('CommentsBreakfast', backref='author', lazy=True)
    dinner = db.relationship('Dinner', backref='author', lazy=True)
    dinnercomments = db.relationship('CommentsDinner', backref='author', lazy=True)
    lunch = db.relationship('Lunch', backref='author', lazy=True)
    lunchcomments = db.relationship('LunchsProduct', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Breakfast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    content= db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('CommentsBreakfast', backref='title', lazy='dynamic')


    def __repr__(self):
        return f"Breakfast('{self.title}', '{self.date_posted}')"

class CommentsBreakfast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("breakfast.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"CommentsBreakfast('{self.comment}', '{self.date_posted}')"

class Dinner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    content= db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('CommentsDinner', backref='title', lazy='dynamic')
    def __repr__(self):
        return f"Dinner('{self.title}', '{self.date_posted}')"

class CommentsDinner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    pickup_id = db.Column(db.Integer, db.ForeignKey("dinner.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"CommentsDinner('{self.comment}', '{self.date_posted}')"

class Lunch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    content= db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('CommentsLunch', backref='title', lazy='dynamic')

    def __repr__(self):
        return f"Lunch('{self.title}', '{self.date_posted}')"

class CommentsLunch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey("lunch.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"CommentsLunch('{self.comment}', '{self.date_posted}')"
