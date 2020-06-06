from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.form import RegistrationForm, LoginForm
import email_validator
from flaskblog.model import User, Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template("registration.html", form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'pass':
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('The username or password is incorrect. Please try again','danger')
    return render_template("login.html", form = form)
