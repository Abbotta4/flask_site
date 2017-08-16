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
            return redirect(url_for('home'))
    flash('Invalid credentials')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            flash('Passwords do not match')
            redirect(url_for('home'))

        for f in otplist:
            if pbkdf2_sha256.verify(, f.otp):
                query = s.query(User).filter(User.username == [POST_USERNAME])
                exist = query.first()
                if not exist:
                    s.query(OTP).filter(OTP.otp == f.otp).delete()
                    s.add(User(POST_USERNAME, pbkdf2_sha256.hash(POST_PASSWORD)))
                    session['logged_in'] = True
                    session['username'] = POST_USERNAME
                    s.commit()
                    return redirect(url_for('home'))
                else:
                    flash('Username already in use')
                    return render_template('register.html')
        flash('Invalid OTP')
        return redirect(url_for('home'))
    else:
        otplist = OTP.query.all()
        for f in otplist:
            
        if request.args['otp'] == 'test':
            return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
