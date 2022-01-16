from app import db,Task
# from models import Task



db.create_all()


task1 = Task(name = 'Fai una todo app')
db.session.add(task1)
task2 = Task(name = 'Metti l\'app su Cloud Run')
db.session.add(task2)
db.session.commit()
    



