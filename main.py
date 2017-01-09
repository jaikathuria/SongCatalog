# Imports Flask
from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
app = Flask(__name__)
import random, string

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError, AccessTokenCredentials 
import httplib2
import json
import requests

# Import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Genre, Songs
# create engine connection with sql library
engine = create_engine('sqlite:///MusicDatabase.db')
#bind the engine with base class
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
conn = DBSession()

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "ItemCatalog"

@app.route('/')
def genreListView():
    genreList = conn.query(Genre).all()
    state  = create_state()
    return render_template('genreList.html',genres = genreList, state = state)

@app.route('/genre/<int:gid>/')
def genreView(gid):
    genre = conn.query(Genre).filter_by(id = gid).one()
    songList = conn.query(Songs).filter_by(g_id = gid)
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
            conn.add(song)
            conn.commit()
            return redirect(url_for('genreView',gid = g_id))
        else:
            return redirect(url_for('newSong',error='incompletefields'))
    genreList = conn.query(Genre).all()
    return render_template('edit.html',genres = genreList)

@app.route('/edit/g/<int:g_id>/s/<int:s_id>',methods=['get','post'])
def editSong(g_id,s_id):
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        url =  request.form['url']
        url = url.replace('watch?v=','embed/')
        url = url.replace('https://','//')
        gid = request.form['genre']
        if name and url and gid:
            song = conn.query(Songs).filter_by(id = s_id,g_id = g_id).one_or_none()
            if song:
                song.name = name
                song.g_id = gid
                song.url = url
                if desc:
                    song.description = desc
                conn.add(song)
                conn.commit()
                return redirect(url_for('genreView',gid = gid))
            else:
                return redirect(url_for('genreListView',error = 'dataNotFound'))
        else:
            return redirect(url_for('newSong',error='incompleteFields'))
    genreList = conn.query(Genre).all()
    song = conn.query(Songs).filter_by(id = s_id,g_id = g_id).one_or_none()
    return render_template('edit.html',genres = genreList,song = song)

@app.route('/delete/g/<int:g_id>/s/<int:s_id>')
def deleteSong(g_id,s_id):
    song = conn.query(Songs).filter_by(id = s_id,g_id = g_id).one_or_none()
    if song:
        conn.delete(song)
        conn.commit()
        return redirect(url_for('genreView',gid = g_id))
    else:
        return redirect(url_for('genreListView',error = 'dataNotFound'))
    
    
@app.route('/view/g/<int:g_id>/s/<int:s_id>')
def viewSong(g_id,s_id):
    song = conn.query(Songs).filter_by(id = s_id,g_id = g_id).one_or_none()
    if song:
        return render_template('view.html',song = song)
    else:
        return redirect(url_for('genreListView',error = 'dataNotFound'))
  

def create_state():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    session['state'] = state
    return state

    
if __name__ == '__main__':
    app.secret_key = 'itstimetomoveon'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)