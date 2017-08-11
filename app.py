from os import urandom
from flask import Flask, flash, redirect, render_template, request, session, abort
from sqlalchemy.orm import sessionmaker
from tabledef import *
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return "Logged in as %s <a href='/logout'>Logout</a>" % (session['username'])

@app.route('/login', methods=['POST'])
def do_login():
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
    return home()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print 'aye, she be POST'
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        POST_OTP = str(request.form['otp'])
        
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(OTP).filter(OTP.otp != None)
        otplist = query.all()
        for f in otplist:
            if pbkdf2_sha256.verify(POST_OTP, f.otp):
                query = s.query(User).filter(User.username.in_([POST_USERNAME]))
                exist = query.first()
                if not exist:
                    s.query(OTP).filter(OTP.otp == f.otp).delete()
                    s.add(User(POST_USERNAME, pbkdf2_sha256.hash(POST_PASSWORD)))
                    session['logged_in'] = True
                    session['username'] = POST_USERNAME
                    s.commit()
                    return home()
                else:
                    flash('Username already in use')
                    return render_template('register.html')
        flash('Invalid OTP')
        return render_template('register.html')
    else:
        'Nay, she be GETtin'
        return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = urandom(12)
    app.run(host='0.0.0.0')
