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

@app.route('/new/',methods=['get','post'])
def newSong():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        url =  request.form['url']
        url = url.replace('watch?v=','embed/')
        url = url.replace('https://','//')
        g_id = request.form['genre']
        if name and url and g_id:
            song = Songs()
            song.name = name
            song.g_id = g_id
            song.url = url
            if desc:
                song.description = desc
            session.add(song)
            session.commit()
            return redirect(url_for('genreView',gid = g_id))
        else:
            return redirect(url_for('newSong',error='incompletefields'))
    genreList = session.query(Genre).all()
    return render_template('edit.html',genres = genreList)

@app.route('/edit/g/<int:g_id>/s/<int:s_id>',methods=['get','post'])
def editSong(g_id,s_id):
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        url =  request.form['url']
        url = url.replace('watch?v=','embed/')
        url = url.replace('https://','//')
        g_id = request.form['genre']
        if name and url and g_id:
            song = session.query(Songs).filter_by(id = s_id,g_id = g_id).one_or_none()
            if song:
                song.name = name
                song.g_id = g_id
                song.url = url
                if desc:
                    song.description = desc
                session.add(song)
                session.commit()
                return redirect(url_for('genreView',gid = g_id))
            else:
                return redirect(url_for('genreListView',error = 'dataNotFound'))
        else:
            return redirect(url_for('newSong',error='incompleteFields'))
    genreList = session.query(Genre).all()
    song = session.query(Songs).filter_by(id = s_id,g_id = g_id).one_or_none()
    return render_template('edit.html',genres = genreList,song = song)

@app.route('/delete/g/<int:g_id>/s/<int:s_id>')
def deleteSong(g_id,s_id):
    song = session.query(Songs).filter_by(id = s_id,g_id = g_id).one_or_none()
    if song:
        session.delete(song)
        session.commit()
        return redirect(url_for('genreView',gid = g_id))
    else:
        return redirect(url_for('genreListView',error = 'dataNotFound'))
    
    
@app.route('/view/g/<int:g_id>/s/<int:s_id>')
def viewSong(g_id,s_id):
    song = session.query(Songs).filter_by(id = s_id,g_id = g_id).one_or_none()
    if song:
        return render_template('view.html',song = song)
    else:
        return redirect(url_for('genreListView',error = 'dataNotFound'))
        

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)