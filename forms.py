from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, TextAreaField, SelectField
from wtforms.validators import DataRequired


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

