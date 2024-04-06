from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import random

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/song_reccomend'
db=SQLAlchemy(app)

class Bts_song(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    song_name= db.Column(db.String(44),nullable=False)
    song_lyrics=db.Column(db.String(44),nullable=False)
    song_genre=db.Column(db.String(44),nullable=False)

@app.route('/')
def index():
    songs=Bts_song.query.all()
    return render_template('index.html',songs=songs)

@app.route('/analyze' , methods=['POST','GET'])
def result():
        user_songs = request.form.getlist('user_songs[]')
        matched_genre=[]
        matched_song=[]
        unique_genres = set()  # Use a set to store unique genres
        for user_song in user_songs:
            check = Bts_song.query.filter_by(song_name=user_song).first()
            matched_genre.append(check.song_genre)
            unique_genres.add(check.song_genre)

            repeated_genres = [genre for genre in matched_genre if matched_genre.count(genre) > 1]

            if unique_genres:
                songs = Bts_song.query.filter(Bts_song.song_genre.in_(unique_genres)).all()
                matched_song = [song.song_name for song in songs]

            # Shuffle the matched songs and select the first 10
            random.shuffle(matched_song)
            matched_song = matched_song[:10]
        
        return render_template('result.html',matched_genre=matched_genre,matched_song=matched_song,repeated_genres=repeated_genres)

if __name__=='__main__':
    db.create_all()
    app.run()