
from flask import render_template, request, redirect, url_for, Response, flash
# import sqlalchemy
from app import app,db
from models import Task, Comment 
from forms import AddTask, AddComment


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


