from flask import Flask, render_template, url_for, flash, redirect
from form import RegistrationForm, LoginForm
import email_validator
app = Flask(__name__)

app.config['SECRET_KEY'] = '5468576D5A713474'

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

@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", form = form)

if __name__ == '__main__':
    app.run(debug=True)