
import os
import json
from flask import render_template, request, redirect, url_for, Response, flash
# import sqlalchemy
from app import app,db
from models import Task, Comment, User
from forms import LoginForm, RegisterForm, AddTask, AddComment, DeleteTask
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from oauthlib.oauth2 import WebApplicationClient
import requests

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Start of new google login code
@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    if not User.query.filter_by(email=users_email).first():
        return redirect(url_for('unauthorized'))
    user = User(
        id=unique_id, name=users_name, email=users_email, profile_pic=picture
    )
    
    # Doesn't exist? Add to database
    if not User.get(unique_id):
        new_user = User.query.filter_by(email=users_email).first()
        new_user.id = unique_id
        new_user.name = users_name
        new_user.profile_pic = picture
        db.session.commit()
#        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route('/', methods = ["GET","POST"])
# @login_required
def index():
    if current_user.is_authenticated:
        tasks = Task.query.join(User).all()
    
        add_task = AddTask()
        if add_task.validate_on_submit():
            new_task = Task(name = add_task.name.data, desc=add_task.desc.data, type=add_task.type.data, author_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("index.html", tasks = tasks, add_task=add_task)
    else:
        return (
            '<p>Utente non autenticato</p>'
            '<a class="button" href="/login">Fai clic per autenticarti con il tuo account Google</a>'
        )
    

@app.route('/activity/<int:id>', methods = ["GET","POST"])
@login_required
def activity(id):
    activity = Task.query.filter_by(id=id).join(User).first()
    comments = Comment.query.filter_by(task_id=id).join(User).all()

    add_comment = AddComment()
    if add_comment.validate_on_submit():
        new_comment = Comment(text = add_comment.text.data, task_id = id, author_id = current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("activity", id=id))

    return render_template ('activity.html', task=activity, comments=comments, add_comment=add_comment)


@app.route('/delete/<int:id>', methods = ["GET","POST"])
@login_required
def delete(id):
    activity = Task.query.filter_by(id=id).join(User).first()
    
    delete_task = DeleteTask()
    if delete_task.validate_on_submit():
        if current_user.id == activity.author.id:
            Comment.query.filter_by(task_id=id).delete()
            db.session.delete(Task.query.get(id))
            db.session.commit()
            return redirect(url_for("index"))
        else:
            flash("Non puoi cancellare l'attività")
    return render_template ('delete.html', task=activity, delete_task=delete_task)

@app.route('/about')
@login_required
def about():
    return render_template ('about.html')

@app.route('/unauthorized')
def unauthorized():
    return render_template ('unauthorized.html')


