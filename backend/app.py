from flask_cors import CORS
from flask_session import Session

from flask import (
    Flask,
    jsonify,
    session,
    request,
    redirect,
    url_for,
    make_response
)

import redis
from redis import RedisError

from spotipy import Spotify, CacheHandler
from spotipy.oauth2 import SpotifyOAuth

from uuid import uuid4

import os
import json
from cryptography.fernet import Fernet
import logging

import utils
from config import AppConfig


# from flask_sqlalchemy import SQLAlchemy

REACT_HOMEPAGE_URL = "http://localhost:5173"

app = Flask(__name__, static_url_path="/", static_folder="./client/build")
app.config.from_object(AppConfig)

server_session = Session(app)

CORS(app, origins=['http://localhost:5173'], supports_credentials=True)

# Encryption key (keep this secret)
encryption_key = os.environ.get("ENCRYPTION_KEY")
cipher = Fernet(encryption_key)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

logger = logging.getLogger(__name__)

# Set up database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# db = SQLAlchemy(app)

class RedisCacheHandler(CacheHandler):
    """
    A cache handler that stores the token info in the Redis.
    """

    def __init__(self, redis, key=None):
        """
        Parameters:
            * redis: Redis object provided by redis-py library
            (https://github.com/redis/redis-py)
            * key: May be supplied, will otherwise be generated
                   (takes precedence over `token_info`)
        """
        self.redis = redis
        self.key = key if key else 'token_info'

    def get_cached_token(self):
        token_info = None
        try:
            token_info = self.redis.get(self.key)
            if token_info:
                return json.loads(token_info)
        except RedisError as e:
            logger.warning('Error getting token from cache: ' + str(e))

        return token_info

    def save_token_to_cache(self, token_info):
        try:
            self.redis.set(self.key, json.dumps(token_info))
        except RedisError as e:
            logger.warning('Error saving token to cache: ' + str(e))

r = redis.Redis()

user_id = uuid4().hex
print("USER ID = ", user_id)
cache_handler = RedisCacheHandler(r, user_id)

# Spotipy oauth
def create_sp_oauth():
    sp_oauth = SpotifyOAuth(
        client_id="b1625933bc024e5aa12e7d262fbf6e46",
        client_secret="b130e9b709c841439515839d8010928c",
        redirect_uri="http://localhost:5173/login",
        scope="user-read-recently-played user-top-read playlist-read-private playlist-modify-private user-read-private",
        cache_handler=cache_handler,
    )
    return sp_oauth

sp_oauth = create_sp_oauth()

# Define Token model
# class Token(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    access_token = db.Column(db.LargeBinary)
#    refresh_token = db.Column(db.LargeBinary)


# # Token refreshment function
# def refresh_access_token():
#     #sp_oauth = create_sp_oauth()
#     token_info = session.get("spotify_token")
#     if token_info:
#         # Decrypt refresh token
#         refresh_token = cipher.decrypt(token_info["refresh_token"]).decode()

#         # Use refresh token to obtain new access token from Spotify
#         new_token_info = sp_oauth.refresh_access_token(refresh_token)

#         print("NEW: ", new_token_info)

#         # Encrypt new access token
#         encrypted_access_token = cipher.encrypt(new_token_info["access_token"].encode())

#         # Update access token in session and database
#         token_info["access_token"] = encrypted_access_token
#         token_info["expires_in"] = new_token_info["expires_in"]

#         session["token_info"] = token_info


@app.route("/")
def index():
    return app.send_static_file("index.html")

#Get auth url
@app.route("/authurl")
def auth_url():
    #sp_oauth = create_sp_oauth()
    # Redirect to Spotify authorization page
    auth_url = sp_oauth.get_authorize_url()

    #return redirect(auth_url)
    return jsonify({"AuthUrl" : auth_url}), 200



#Login route
@app.route("/login", methods=["POST"])
def login():

    if request.args.get("code"):
        code = request.args.get("code")
        print("code = ", code)
        token_info = sp_oauth.cache_handler.get_cached_token()
        print(token_info)
        if token_info is None:  
            token_info = sp_oauth.get_access_token(code, check_cache=True)
            print("Access token: ", token_info)
            sp_oauth.cache_handler.save_token_to_cache(token_info)

        #session[user_id] = token_info
        #encrypted_token = cipher.encrypt(token_info["access_token"].encode())
        response = jsonify({"id" : user_id}), 200
        return response
    else:
        return jsonify({"Error":"Failed to authenticate"}), 500
            
    


# Logout route
@app.route("/logout", methods = ["POST"])
def logout():
    # Clear cached token information from session
    data = request.get_json()
    if "id" in data:
        id = data["id"]
        print("\n\nID IS = ", id)
        #session.pop(id)
        r.delete(id)
        print(r.keys())

    # Clear token information from the database
    #    Token.query.delete()
    #    db.session.commit()

    return jsonify({"Status":"OK"}), 200


# callback() function is responsible for handling this redirect. It extracts the authorization code from the URL and exchanges it for an access token
# (and possibly a refresh token) with the OAuth2 provider (Spotify) using your application's client ID, client secret, and other necessary parameters.


# @app.route("/callback")
# def callback():
#     sp_oauth = create_sp_oauth()
#     if request.args.get("code") or sp_oauth.validate_token(
#         sp_oauth.get_cached_token()
#     ):
#         _ = sp_oauth.get_access_token(request.args.get("code"))
#         user_session = session.get("spotify_token")

#         print("spotify token: ", user_session)
#         # encrypted_token = cipher.encrypt(user_session["access_token"].encode())
#         # response = jsonify({"Bearer":str(encrypted_token)}), 200
#         return redirect(REACT_HOMEPAGE_URL)
#     else:
#         return jsonify({"Error":"Failed to authenticate"}), 500


@app.route("/logged")
def logged():
    token_info = sp_oauth.cache_handler.get_cached_token() is not None
    response = jsonify({"Authenticated":token_info}), 200
    return response
    


@app.route("/api/v1/recommendations/recently-played")
def recently_played_recommendations():
    # Check if user is authenticated
    if 'token_info' not in session:
        return redirect(url_for('login'))
    
    # Decrypt tokens before using them
    token_info = session.get("spotify_info")
    decrypted_access_token = cipher.decrypt(token_info['access_token']).decode()

    # Initialize Spotipy with the access token
    sp = Spotify(auth=decrypted_access_token)

    # Fetch recently played tracks
    recommended_json = utils.recommended(sp, 50, mode="rp")
    return recommended_json



@app.route("/api/v1/recommendations/top-tracks")
def top_tracks_recommendations():
    # Check if user is authenticated
    if 'token_info' not in session:
        return redirect(url_for('login'))
    
    # Decrypt tokens before using them
    token_info = session['token_info']
    decrypted_access_token = cipher.decrypt(token_info['access_token']).decode()

    # Initialize Spotipy with the access token
    sp = Spotify(auth=decrypted_access_token)

    # Fetch recently played tracks
    recommended_json = utils.recommended(sp, 50, mode="tt")
    return recommended_json    


@app.route("/api/v1/recommendations/my-playlists")
def my_playlists():
    # Check if user is authenticated
    if 'token_info' not in session:
        return redirect(url_for('login'))
    
    # Decrypt tokens before using them
    token_info = session['token_info']
    decrypted_access_token = cipher.decrypt(token_info['access_token']).decode()

    # Initialize Spotipy with the access token
    sp = Spotify(auth=decrypted_access_token)

    # Fetch recently played tracks
    user_playlists = sp.current_user_playlists(limit = 50, offset=0)
    
    playlist_items = []
    keys = ["playlist_id", "playlist_name", "image_url"]
    for playlist in user_playlists['items']:
        playlist_id = playlist['id']
        playlist_name = playlist['name']
        playlist_image_url = playlist['images'][-1]['url'] if playlist['images'] else ''  # Get the first image URL if available
        playlist_items.append(dict(zip(keys, [playlist_id, playlist_name, playlist_image_url])))

    return json.dumps(playlist_items)



@app.route('/api/v1/recommendations/playlist/<playlist_id>')
def my_playlist_recommendations(playlist_id):
    # Check if user is authenticated
    if 'token_info' not in session:
        return redirect(url_for('login'))

    # Decrypt tokens before using them
    token_info = session['token_info']
    decrypted_access_token = cipher.decrypt(token_info['access_token']).decode()

    # Initialize Spotipy with the access token
    sp = Spotify(auth=decrypted_access_token)
    username = sp.current_user()["id"]

    # Fetch tracks from the selected playlist
    recommended_json = utils.recommended(sp, limit=50, mode="in", track_name=playlist_id, username=username)

    # Process the tracks and get suggestions for similar tracks
    # You can implement this part using Spotipy's recommendation endpoints

    return recommended_json


@app.route('/api/v1/recommendations/track')
def track_recommendations():
    # Check if user is authenticated
    if 'token_info' not in session:
        return redirect(url_for('login'))

    # Decrypt tokens before using them
    token_info = session['token_info']
    decrypted_access_token = cipher.decrypt(token_info['access_token']).decode()

    track_name = request.args.get("name")
    artist_name = request.args.get("artist")
    
    # Initialize Spotipy with the access token
    sp = Spotify(auth=decrypted_access_token)
    
    if artist_name != None:
        recommended_json = utils.recommended(sp, limit=50, mode="in", track_name=track_name, artist_name=artist_name)
    else:
        recommended_json = utils.recommended(sp, limit=50, mode="in", track_name=track_name)    
    
    return recommended_json




@app.route('/api/v1/recommendations/playlist')
def playlist_recommendations():
    # Check if user is authenticated
    if 'token_info' not in session:
        return redirect(url_for('login'))

    # Decrypt tokens before using them
    token_info = session['token_info']
    decrypted_access_token = cipher.decrypt(token_info['access_token']).decode()

    playlist_url = request.args.get("url")
    
    # Initialize Spotipy with the access token
    sp = Spotify(auth=decrypted_access_token)
    username = sp.current_user()["id"]

    recommended_json = utils.recommended(sp, limit=20, mode="in", track_name=playlist_url, username=username)

    
    return recommended_json



if __name__ == "__main__":
    app.run(debug=True)
