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
  
@app.route('/gconnect', methods = ['post'])
def gconnect():
    if request.args.get('state') != session['state']:
        response.make_response(json.dumps('Invalid State paramenter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json',scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response.make_response(json.dumps('Failed to upgrade the authorisation code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    header = httplib2.Http()
    result = json.loads(header.request(url, 'GET')[1])
    
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    session['credentials'] = access_token
    session['gplus_id'] = gplus_id
    
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    
    data = answer.json()

    session['name'] = data['name']
    session['img'] = data['picture']
    session['email'] = data['email']
    
    return jsonify(name = session['name'],email = session['email'], img = session['img'])        

def create_state():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    session['state'] = state
    return state

    
if __name__ == '__main__':
    app.secret_key = 'itstimetomoveon'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)