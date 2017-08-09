import os
from flask import Flask, flash, redirect, render_template, request, session, abort
from sqlalchemy.orm import sessionmaker
from tabledef import *
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
#engine = create_engine('postgresql://postgres:postgres@localhost/tutorial', echo=True)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Logged in as %s <a href='/logout'>Logout</a>" % (session['username'])

@app.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]))
    result = query.first()
    if result:
        accept = pbkdf2_sha256.verify(POST_PASSWORD, result.password)
        if accept:
            session['logged_in'] = True
            session['username'] = POST_USERNAME
            return home()
    flash('Invalid credentials')
    return home()

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You have logged out')
    return home()

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
