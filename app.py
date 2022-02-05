import os
from flask import Flask
# import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import pymysql


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'


# Connection String Old Style
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
environ = os.environ["ENVIRON"]
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + db_user + ':' + db_pass + '@/' + db_name + '?unix_socket=' + db_socket_dir + '/' + instance_connection_name


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from routes import *
from models import *

db.create_all()



if __name__ == "__main__":
#    if environ == 'test':
  app.run(debug=True, host="127.0.0.1", port=5000)
#    else:
#        app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    
