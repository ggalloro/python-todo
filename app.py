import os
import datetime
import logging
from flask import Flask, render_template, request, redirect, url_for, Response, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, TextAreaField, SelectField
from wtforms.validators import DataRequired, AnyOf
# import sqlalchemy
from sqlalchemy import ForeignKey, create_engine, MetaData, Table, Column, Integer, String, insert
from sqlalchemy.sql import select
# from flask_sqlalchemy import SQLAlchemy
import pymysql



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

# Connection using SQLAlchemy with native (non SQL) commands
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
environ = os.environ["ENVIRON"]
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
engine = create_engine('mysql+pymysql://' + db_user + ':' + db_pass + '@/' + db_name + '?unix_socket=' + db_socket_dir + '/' + instance_connection_name, echo=True, future=True)
metadata_obj = MetaData()


# Create table w Expression Language
task = Table(
    "task",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(80)),
    Column('desc', String(255)),
    Column('type', String(30)),
    Column('author', String(20))
)

comment = Table(
    "comment",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('text', String(255)),
    Column('task', ForeignKey('task.id'))
)

metadata_obj.create_all(engine)

types = [("Mangiare","Mangiare"),("Parco / Aria aperta","Parco / Aria aperta"),("Museo / Mostra","Museo / Mostra"), ("Vacanza","Vacanza")]
authors = ['Mamma','Papà','Figlio','Figlia']

class AddTask(FlaskForm):
    name = StringField("Nome Attività", validators = [DataRequired(message="Inserire il nome dell'attività")])
    desc = TextAreaField("Descrizione e (eventuale) link")
    type = RadioField("Tipo", choices=types)
    # author = StringField("Proponente:", validators = [AnyOf(authors, message="Il proponente deve essere un componente della famiglia: %(values)s")])
    author = SelectField("Proponente:", choices = authors)
    submit = SubmitField("Aggiungi Attività")

class AddComment(FlaskForm):
    text = TextAreaField("Commento", validators = [DataRequired()])
    submit = SubmitField("Aggiungi Commento")

@app.route('/', methods = ["GET","POST"])
def index():
    conn = engine.connect()
    s = select(task)
    result = conn.execute(s)
    tasks = [row for row in result]

    add_task = AddTask()
    if add_task.validate_on_submit():
        new_name = add_task.name.data
        new_desc = add_task.desc.data
        new_type= add_task.type.data
        new_author = add_task.author.data
        ins = task.insert()
        conn = engine.connect()
        result = conn.execute(ins,{"name": new_name, "desc": new_desc, "type": new_type, "author": new_author})
        conn.commit()
        return redirect('/')
    return render_template("index.html", tasks=tasks, add_task=add_task)

@app.route('/activity/<int:id>', methods = ["GET","POST"])
def activity(id):
    conn = engine.connect()
    s = select(task).where(task.c.id == id)
    result = conn.execute(s)
    activity = [row for row in result]
    
    selcom = select(comment).where(comment.c.task == id)
    comments = [row for row in conn.execute(selcom)]

    add_comment = AddComment()
    if add_comment.validate_on_submit():
        comment_text = add_comment.text.data
        ins = comment.insert()
        conn = engine.connect()
        result = conn.execute(ins,{"text": comment_text, "task": id})
        conn.commit()
        return redirect(url_for("activity", id=id))
    return render_template ('activity.html', task=activity[0], comments=comments, add_comment=add_comment)

@app.route('/about')
def about():
    return render_template ('about.html')

if __name__ == "__main__":
    if environ == 'test':
        app.run(debug=True, host="127.0.0.1", port=5000)
    else:
        app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

    



