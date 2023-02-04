from flask import Flask, render_template,request, session, redirect, url_for, render_template_string, send_file, flash
import requests
import numpy as np
import pandas as pd
import pandas_datareader as data
import webbrowser
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField
from wtforms.validators import InputRequired, Email, Length 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import time


app = Flask(__name__)
db = SQLAlchemy()

app.config['SECRET_KEY'] = 'hetjainikproject'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///psc_innovative.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self):
        return (self.sno)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.username} - {self.date_created}"

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class SignupForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    terms = BooleanField('terms')

class WatchListForm(FlaskForm):
    stock_ticker = StringField('stock_ticker', validators=[InputRequired(), Length(min=3)])
    start = DateField('start_date', format='%Y-%m-%d')
    end = DateField('end_date', format='%Y-%m-%d')



@app.route("/")
#@login_required
def home():
    return render_template('index.html')

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route("/watchlist", methods=["GET","POST"])
#@login_required
def watchlist():
    form = WatchListForm()
    if form.validate_on_submit():
        stock_ticker = form.stock_ticker.data
        start = form.start.data
        end = form.start.data
        url = "https://finance.yahoo.com/quote/"+ stock_ticker
        stocks = pd.read_html(url)
        df = stocks[2]
        df = df.reset_index(drop=True)
        
        return render_template("frame.html", tables=[df.to_html(classes='data')], titles=df.columns.values)
    return render_template('watchlist.html', form=form)

@app.route("/news")
def news():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=80b9296f0fc04925802ef77f48e124f7"
    page = ''
    while page == '':
        try:
            page = requests.get(url).json()
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

    case  = {
        'articles' : page['articles']
    }
    return render_template('news.html', cases = case)
    

@app.route("/help")
def help():
    return render_template('help.html')

@app.route("/frame")
def frame():
    return render_template('frame.html')

@app.route("/creators")
def creators():
    return render_template('creators.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username = form.username.data, email= form.email.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit() 
        return redirect(url_for('home'))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html',form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)