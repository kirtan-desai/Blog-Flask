from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.form import RegistrationForm, LoginForm
import email_validator
from flaskblog.model import User, Post
from flask_login import login_user, current_user, logout_user

posts = [
    {
        'author':'Charles Bukowski',
        'title':'Evolution of life',
        'content':'Lorem ipsum doooba',
        'date_posted':'June 5, 2020',
    },
    {
        'author':'Merlinda Royce',
        'title':'The black hole no one talks about',
        'content':'George Floyd was killed',
        'date_posted':'June 7, 2020',
    }

] 

@app.route('/home')
@app.route('/')
def home():
    return render_template("index.html", posts=posts, title = 'Temp')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now login using your username and password.','success')
        return redirect(url_for('login'))
    return render_template("registration.html", form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('The email or password is incorrect. Please try again','danger')
    return render_template("login.html", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))