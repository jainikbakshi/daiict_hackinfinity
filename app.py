from flask import Flask, render_template,request, session, redirect, url_for, render_template_string, send_file, flash
import requests
from flask_sqlalchemy import SQLAlchemy
from pytube import YouTube, Playlist
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from io import BytesIO
import youtube_dl
from turtle import down
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


@app.route("/")
#@login_required
def home():
    return render_template('index.html')

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route("/wishlist")
@login_required
def wishlist():
    return render_template('wishlist.html')

# new changes for the playlist download are made here
#@app.route("/youtube_playlist", methods= ['GET', 'POST'])
#def youtube_playlist_download():
#    if request.method == "POST":
#        downloaded = False
#        url = request.form.get('youtube_playlist_download')
#        playl = Playlist(url)
#        for videos in playl.videos:
#            videos.streams.first().download()
#        downloaded = True
    # flash('Playlist ' + playl.title + ' downloaded successfully!')
    # return render_template('index.html', py = playl, d_check = downloaded )
#    return render_template('playlist.html', py = playl)

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
    

# @app.route("/youtube/playlist", methods = ['GET','POST'])
# def youtube_playlist_download():
    # if request.method == "POST":
    #     link = request.form.get('youtube_playlist_download')
    #     playlist = Playlist(link)
    #     for video in playlist.videos:
    #         video.streams.first().download()
    # return redirect(url_for('youtube'))
    # if request.method == "POST":
    #     buffer = BytesIO()
    #     link = request.form.get('youtube_playlist_download')
    #     playlist = Playlist(link)
    #     # url = YouTube(session['link'])
    #     # itag = request.form.get('itag')
    #     # video = url.streams.get_by_itag(itag)
    #     for video in playlist.videos:
    #         # video.stream_to_buffer(buffer)
    #         buffer.seek(0)
    #         return send_file(buffer, as_attachment=True, download_name=(link.title+'.mp4'))
    # return redirect(url_for('base'))
        

#@app.route("/youtube" , methods = ['GET', 'POST'])
#def youtube():
    #this portion of code check the validity of the youtube link 
#    if request.method == 'POST':
#        session['link'] = request.form.get('youtube_link')
#        try:
#            check_link = YouTube(session['link'])
#            check_link.check_availability()
#        except:
#            return render_template('errorPage.html')
#        return render_template('youtube_download.html', url = check_link) #ye line me we passed url so that we could use it in the youtube_download wali
#    return render_template('youtube.html')

#@app.route("/youtube/download" , methods = ["GET", "POST"])
#def youtube_video_download():
#    if request.method == "POST":
#        buffer = BytesIO()
#        url = YouTube(session['link'])
#        itag2 = request.form.get('itag')
        # video = url.streams.get_by_itag(18)
#        video = url.streams.get_by_itag(itag2)
#        video.stream_to_buffer(buffer)
#        buffer.seek(0)
#        return send_file(buffer, as_attachment=True, download_name=(url.title+'.mp4'))
#    return redirect(url_for('base'))

#@app.route("/youtube/downloadmp3" , methods = ["GET", "POST"])
#def youtube_mp3_download():
#    if request.method == "POST":
#        buffer = BytesIO()
#        url = YouTube(session['link'])
#        audio = url.streams.filter(only_audio=True).first()
#        audio.stream_to_buffer(buffer)
#        buffer.seek(0)
#       return send_file(buffer, as_attachment=True, download_name=(url.title+'.mp3'))
#    return redirect(url_for('base'))


#@app.route("/instagram") 
#def instagram():
#    return render_template('instagram.html')

#@app.route("/facebook")
#def facebook():
#    return render_template('facebook.html')

# @app.route("/facebook/download" , methods = ["GET", "POST"])
# def facebook_video_download():
#     # link = request.form['facebook_link']
#     # itag = int(999)
#     # with youtube_dl.YoutubeDL() as ydl:
#     #     url = ydl.extract_info(link, download=False)
#     #     downloadLink = (url["formats"][itag]["url"])
#     # return redirect(downloadLink+"&dl=1")
#     url = request.form.get('facebook_link')
#     with youtube_dl.YoutubeDL() as ydl:
#         link = ydl.extract_info(url, download=False)
#         try:
#             download_link = link["entries"][-1]["formats"][-1]["facebook_link"]
#         except: 
#             download_link = link["formats"][-1]["facebook_link"]
#         return redirect(download_link+"&dl=1")
#@app.route('/facebook/download', methods=["POST", "GET"])
#def facebook_download():
#	url = request.form["url"]
# 	print("Someone just tried to download", url)
#	with youtube_dl.YoutubeDL() as ydl:
#		link = ydl.extract_info(url, download=False)
# 		print(url)
#		try:
#			download_link = link["entries"][-1]["formats"][-1]["url"]
#		except:
#			download_link = link["formats"][-1]["url"]
#		return redirect(download_link+"&dl=1")
    

#@app.route("/result")
#def home1():
    # if request.method == 'POST':
    #     session['link'] = request.form.get('url')
    #     try:
    #         url = YouTube(session['link'])
    #         url.check_availability() 
    #     except:
    #         return render_template('error.html')
    #     return render_template('Download.html')
    # return render_template('index.html')

@app.route("/help")
def help():
    return render_template('help.html')

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