from os import urandom
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from tabledef import db, User, OTP
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/tutorial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return "Logged in as %s <a href='/logout'>Logout</a>" % (session['username'])

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    query = User.query.filter_by(username=username)
    result = query.first()
    if result:
        accept = pbkdf2_sha256.verify(password, result.password)
        if accept:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
    flash('Invalid credentials')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            flash('Passwords do not match')
            return redirect(url_for('home'))
        db.session.add(User(username, pbkdf2_sha256.hash(password)))
        session['logged_in'] = True
        session['username'] = username
        db.session.commit()
        return redirect(url_for('home'))
    else:
        otplist = OTP.query.all()
        for f in otplist:
            if pbkdf2_sha256.verify(request.args['otp'], f.otp):
                db.session.delete(OTP.query.filter_by(otp=f.otp))
                return render_template('register.html')
        flash('Invalid OTP')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
