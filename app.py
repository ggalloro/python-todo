import os
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
class AddTask(FlaskForm):
    task = StringField("Task", validators = [DataRequired()])
    submit = SubmitField("Aggiungi Task")


todos = ["Fai un app per ristoranti","Deploya su Cloud run"]

@app.route('/', methods = ["GET","POST"])
def index():
    add_task = AddTask()
    if add_task.validate_on_submit():
        todos.append(add_task.task.data)
        return redirect('/')
    return render_template("index.html", todos = todos, add_task=add_task)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    



