from app import db
from models import User

ids = User.query.count()
userid = 1000 + ids
print("\nScript per abilitare utenti all'accesso mediante account Google\n")
emails = input('Inserisci le email degli account Google da abilitare separate da virgola: ').split(",")

for email in emails:
    userid += 1
    user = User(id = str(userid), email=email)
    db.session.add(user)
db.session.commit()
print("Account abilitati all'accesso")

