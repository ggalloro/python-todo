from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index = True)
    desc = db.Column(db.String(255), index = True)
    type = db.Column(db.String(30), index = True)
    author_id = db.Column(db.String(100), db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref = 'task', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(255), index = True)
    author_id = db.Column(db.String(100), db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

class User(UserMixin, db.Model):
    id = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(50), index = True)
    email = db.Column(db.String(50), index = True, unique = True)
    profile_pic = db.Column(db.String(120), index = True)
    tasks = db.relationship('Task', backref = 'author', lazy=True)
    comments = db.relationship('Comment', backref = 'author', lazy=True)
    
    @staticmethod
    def get(user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        return user

    @staticmethod
    def create(id, name, email, profile_pic):
        new_user = User(id=id, name=name, email=email,profile_pic=profile_pic)
        db.session.add(new_user)
        db.session.commit()

    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@login.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


