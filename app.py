import os
import datetime
import logging
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + db_user + ':' + db_pass + '@/' + db_name + '?unix_socket=' + db_socket_dir + '/' + instance_connection_name

# Code to connect to CloudSQL taken from Cloud Run docs
# Removed since it uses different code
# End of code from Google Docs

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index = True)
class AddTask(FlaskForm):
    task = StringField("Task", validators = [DataRequired()])
    submit = SubmitField("Aggiungi Task")

db.create_all()


@app.route('/', methods = ["GET","POST"])
def index():
    tasks = Task.query.all()
    add_task = AddTask()
    if add_task.validate_on_submit():
        new_task = Task(name = add_task.task.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    return render_template("index.html", tasks = tasks, add_task=add_task)

# Code to run as a server in GKE/Cloudrun
if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    



