# Imports Flask
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


# Import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Genre, Songs
# create engine connection with sql library
engine = create_engine('sqlite:///MusicDatabase.db')
#bind the engine with base class
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
def genreListView():
    genreList = session.query(Genre).all()
    return render_template('genreList.html',genres = genreList)


@app.route('/genre/<int:gid>/')
def genreView(gid):
    genre = session.query(Genre).filter_by(id = gid).one()
    songList = session.query(Songs).filter_by(g_id = gid)
    return render_template('genre.html',songs = songList,genre = genre)
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)