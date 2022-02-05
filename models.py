from app import db



class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index = True)
    desc = db.Column(db.String(255), index = True)
    type = db.Column(db.String(30), index = True)
    author = db.Column(db.String(20), index = True)
    comments = db.relationship('Comment', backref = 'task', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(255), index = True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))


    
