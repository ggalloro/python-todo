import os
import datetime
import logging
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
from sqlalchemy.sql import select
# from flask_sqlalchemy import SQLAlchemy
import pymysql



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

# Connection using SQLAlchemy with native (non SQL) commands
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
engine = create_engine('mysql+pymysql://' + db_user + ':' + db_pass + '@/' + db_name + '?unix_socket=' + db_socket_dir + '/' + instance_connection_name, echo=True, future=True)
metadata_obj = MetaData()




#Create tables w SQLAlchemy

# Using SQL Language
# @app.before_first_request
# def create_tables():
#    global db
#    db = db or init_connection_engine()
    # Create tables (if they don't already exist)
#    with db.connect() as conn:
#        conn.execute(
#            "CREATE TABLE IF NOT EXISTS task "
#            "( id int, name varchar(120), PRIMARY KEY (id) );"
#        )

# Create table w Expression Language
task = Table(
    "task",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(120))
)

metadata_obj.create_all(engine)

class AddTask(FlaskForm):
    task = StringField("Task", validators = [DataRequired()])
    submit = SubmitField("Aggiungi Task")

@app.route('/', methods = ["GET","POST"])
def index():
    conn = engine.connect()
    s = select(task)
    result = conn.execute(s)
    tasks = [row.name for row in result]
    add_task = AddTask()
    if add_task.validate_on_submit():
        new_task = add_task.task.data
        ins = task.insert()
        conn = engine.connect()
        result = conn.execute(ins,{"name": new_task})
        conn.commit()
        return redirect('/')
    return render_template("index.html", tasks = tasks, add_task=add_task)


if __name__ == "__main__":
# Code to run as a server in GKE/Cloudrun
#   app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Code to test locally
    app.run(debug=True, host="127.0.0.1", port=5000)

    



