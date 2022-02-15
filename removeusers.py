from app import db
from models import User


print("\nScript per disabilitare accesso ad utenti\n")
emails = input('Inserisci le email degli account Google da disabilitare separate da virgola: ').split(",")

for email in emails:
    User.query.filter_by(email=email).delete()
db.session.commit()
print("Account disabilitati")

