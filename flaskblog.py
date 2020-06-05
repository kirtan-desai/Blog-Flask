from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from form import RegistrationForm, LoginForm
import email_validator
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5468576D5A713474'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jp')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author',lazy=True)

    def __repr__(self): # This string will be returned on a database query
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable='False')

    def __repr__(self):
        return f"Post('{self.title}','{self.content}')"

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

if __name__ == '__main__':
    app.run(debug=True)