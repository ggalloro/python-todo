from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index = True)
    desc = db.Column(db.String(255), index = True)
    type = db.Column(db.String(30), index = True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref = 'task', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(255), index = True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), index = True)
    surname = db.Column(db.String(50), index = True)
    email = db.Column(db.String(50), index = True, unique = True)
    passwordhash = db.Column(db.String(255), index = True)
    tasks = db.relationship('Task', backref = 'author', lazy=True)
    comments = db.relationship('Comment', backref = 'author', lazy=True)
    
    def set_password(self, password):
        self.passwordhash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

