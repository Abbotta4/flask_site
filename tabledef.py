from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """"""
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password

class OTP(db.Model):
    """"""
    __tablename__ = "otp"

    id = db.Column(db.Integer, primary_key=True)
    otp = db.Column(db.String)

if __name__ == 'main':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/tutorial'
    db.create_all()
