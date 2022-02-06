from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, TextAreaField, SelectField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


types = [("Mangiare","Mangiare"),("Parco / Aria aperta","Parco / Aria aperta"),("Museo / Mostra","Museo / Mostra"), ("Vacanza","Vacanza")]
# authors = ['Mamma','Papà','Figlio','Figlia']

class AddTask(FlaskForm):
    name = StringField("Nome Attività", validators = [DataRequired(message="Inserire il nome dell'attività")])
    desc = TextAreaField("Descrizione e (eventuale) link")
    type = RadioField("Tipo", choices=types)
#    author = SelectField("Proponente:", choices = authors)
    submit = SubmitField("Aggiungi Attività")

class AddComment(FlaskForm):
    text = TextAreaField("Commento", validators = [DataRequired()])
    submit = SubmitField("Aggiungi Commento")

class RegisterForm(FlaskForm):
    name = StringField("Nome", validators = [DataRequired()])
    surname = StringField("Cognome", validators = [DataRequired()])
    email = StringField("Indirizzo email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField("Conferma Password", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField("Registra Utente")

class LoginForm(FlaskForm):
    email = StringField("Indirizzo email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

