
from flask import render_template, request, redirect, url_for, Response, flash
# import sqlalchemy
from app import app,db
from models import Task, Comment, User
from forms import AddTask, AddComment, RegisterForm, LoginForm
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse


@app.route('/register' , methods = ["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name = form.name.data, surname = form.surname.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulazioni, registrazione eseguita con successo !')
    return render_template ('register.html', form = form)


@app.route('/login' , methods = ["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Credenziali non valide')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc:
            next_page = url_for('index')
        return redirect (next_page)
    return render_template ('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods = ["GET","POST"])
@login_required
def index():
    # commented the following to try the join to get author name from task table
    # tasks = Task.query.all()
    # tasks = Task.query.join(User, User.id == Task.author_id).add_columns(Task.name, Task.type, User.name).all()
    # another attempt
    tasks = Task.query.join(User).all()
    
    add_task = AddTask()
    if add_task.validate_on_submit():
        new_task = Task(name = add_task.name.data, desc=add_task.desc.data, type=add_task.type.data, author_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    return render_template("index.html", tasks = tasks, add_task=add_task)

@app.route('/activity/<int:id>', methods = ["GET","POST"])
@login_required
def activity(id):
    # commented to try Join to show user name
    # activity = Task.query.filter_by(id=id).first()
    activity = Task.query.filter_by(id=id).join(User).first()
    
    comments = Comment.query.filter_by(task_id=id).join(User).all()

    add_comment = AddComment()
    if add_comment.validate_on_submit():
        new_comment = Comment(text = add_comment.text.data, task_id = id, author_id = current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("activity", id=id))

    return render_template ('activity.html', task=activity, comments=comments, add_comment=add_comment)

@app.route('/about')
@login_required
def about():
    return render_template ('about.html')


