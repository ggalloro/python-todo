import os
import datetime
import logging
from flask import Flask, render_template, request, redirect, url_for, Response, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, TextAreaField, SelectField
from wtforms.validators import DataRequired
# import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import pymysql



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'



# Connection String Old Style
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
environ = os.environ["ENVIRON"]
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + db_user + ':' + db_pass + '@/' + db_name + '?unix_socket=' + db_socket_dir + '/' + instance_connection_name


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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

db.create_all()

types = [("Mangiare","Mangiare"),("Parco / Aria aperta","Parco / Aria aperta"),("Museo / Mostra","Museo / Mostra"), ("Vacanza","Vacanza")]
authors = ['Mamma','Papà','Figlio','Figlia']

class AddTask(FlaskForm):
    name = StringField("Nome Attività", validators = [DataRequired(message="Inserire il nome dell'attività")])
    desc = TextAreaField("Descrizione e (eventuale) link")
    type = RadioField("Tipo", choices=types)
    author = SelectField("Proponente:", choices = authors)
    submit = SubmitField("Aggiungi Attività")

class AddComment(FlaskForm):
    text = TextAreaField("Commento", validators = [DataRequired()])
    submit = SubmitField("Aggiungi Commento")

@app.route('/', methods = ["GET","POST"])
def index():
    tasks = Task.query.all()
    
    add_task = AddTask()
    if add_task.validate_on_submit():
        new_task = Task(name = add_task.name.data, desc=add_task.desc.data, type=add_task.type.data, author=add_task.author.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    return render_template("index.html", tasks = tasks, add_task=add_task)

@app.route('/activity/<int:id>', methods = ["GET","POST"])
def activity(id):
    activity = Task.query.filter_by(id=id).first()
    
    comments = Comment.query.filter_by(task_id=id).all()

    add_comment = AddComment()
    if add_comment.validate_on_submit():
        new_comment = Comment(text = add_comment.text.data, task_id = id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("activity", id=id))

    return render_template ('activity.html', task=activity, comments=comments, add_comment=add_comment)

@app.route('/about')
def about():
    return render_template ('about.html')

if __name__ == "__main__":
    if environ == 'test':
        app.run(debug=True, host="127.0.0.1", port=5000)
    else:
        app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    
