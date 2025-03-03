from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Repos/rom-cs50/rigops.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456'  # Required for session management

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Initialize bcrypt

# Import routes after initializing db
from routes import *

if __name__ == '__main__':
    app.run(debug=True)