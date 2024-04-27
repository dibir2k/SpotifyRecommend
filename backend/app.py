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

from spotipy import Spotify, CacheHandler
from spotipy.oauth2 import SpotifyOAuth

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

# Set up database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# db = SQLAlchemy(app)

class CacheSessionHandler(CacheHandler):
    def __init__(self, session, token_key):
        self.token_key = token_key
        self.session = session

    def get_cached_token(self):
        return self.session.get(self.token_key)

    def save_token_to_cache(self, token_info):
        self.session[self.token_key] = token_info
        session.modified = True

cache_handler = CacheSessionHandler(session, "spotify_token") 


# Spotipy oauth
def create_sp_oauth():
    sp_oauth = SpotifyOAuth(
        client_id="b1625933bc024e5aa12e7d262fbf6e46",
        client_secret="b130e9b709c841439515839d8010928c",
        redirect_uri="http://127.0.0.1:5000/callback",
        scope="user-read-recently-played user-top-read playlist-read-private playlist-modify-private user-read-private",
        cache_handler=cache_handler,
    )
    return sp_oauth

# Define Token model
# class Token(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    access_token = db.Column(db.LargeBinary)
#    refresh_token = db.Column(db.LargeBinary)


# Token refreshment function
def refresh_access_token():
    sp_oauth = create_sp_oauth()
    token_info = session.get("spotify_token")
    if token_info:
        # Decrypt refresh token
        refresh_token = cipher.decrypt(token_info["refresh_token"]).decode()

        # Use refresh token to obtain new access token from Spotify
        new_token_info = sp_oauth.refresh_access_token(refresh_token)

        print("NEW: ", new_token_info)

        # Encrypt new access token
        encrypted_access_token = cipher.encrypt(new_token_info["access_token"].encode())

        # Update access token in session and database
        token_info["access_token"] = encrypted_access_token
        token_info["expires_in"] = new_token_info["expires_in"]

        session["token_info"] = token_info


# # Index route
# @app.route("/")
# def index():
#     if "token_info" not in session:
#         return redirect(url_for("login"))

#     # Check if token is expired or about to expire
#     token_info = session["token_info"]

#     access_token = cipher.decrypt(token_info["access_token"]).decode()
#     if not access_token or sp_oauth.is_token_expired(token_info):
#         refresh_access_token()

#     # Token is valid, continue with application logic

#     access_token = cipher.decrypt(token_info["access_token"]).decode()
    

#     return jsonify({"message": "Welcome to my Song Recommendation App"})

@app.route("/")
def index():
    return app.send_static_file("index.html")

#Login route
@app.route("/login")
def login():
    # if sp_oauth.validate_token(sp_oauth.get_cached_token()):
    user_session = session.get("spotify_token")
    if user_session:
        print("spotify token: ", user_session)
        encrypted_token = cipher.encrypt(user_session["access_token"].encode())
        return jsonify({"Bearer":str(encrypted_token)}), 200
            
    sp_oauth = create_sp_oauth()
    # Redirect to Spotify authorization page
    auth_url = sp_oauth.get_authorize_url()

    #return redirect(auth_url)

    return jsonify({"url":auth_url}), 200


# Logout route
@app.route("/logout")
def logout():
    # Clear cached token information from session
    session.pop("token_info", None)

    # Clear token information from the database
    #    Token.query.delete()
    #    db.session.commit()

    return redirect(url_for("login"))


# callback() function is responsible for handling this redirect. It extracts the authorization code from the URL and exchanges it for an access token
# (and possibly a refresh token) with the OAuth2 provider (Spotify) using your application's client ID, client secret, and other necessary parameters.


@app.route("/callback")
def callback():
    sp_oauth = create_sp_oauth()
    if request.args.get("code") or sp_oauth.validate_token(
        sp_oauth.get_cached_token()
    ):
        _ = sp_oauth.get_access_token(request.args.get("code"))
        session.get("spotify_info")

        print("\nsession[token_info] (callback) = ", session.get("spotify_token"), "\n")

        return redirect(url_for("login"))
        
    return jsonify({"ERROR":"Could not get token"})

# Callback route
# @app.route("/callback")
# def callback():
#     # Extract authorization code from the request
#     auth_code = request.args.get('code')

#     # Exchange authorization code for tokens
#     token_url = 'https://accounts.spotify.com/api/token'
#     token_data = {
#         'grant_type': 'authorization_code',
#         'code': auth_code,
#         'redirect_uri': 'http://127.0.0.1:5000/callback',
#         'client_id': 'b1625933bc024e5aa12e7d262fbf6e46',
#         'client_secret': 'b130e9b709c841439515839d8010928c',
#     }
#     response = requests.post(token_url, data=token_data)
#     token_info = response.json()

#     # Encrypt tokens
#     encrypted_access_token = cipher.encrypt(token_info["access_token"].encode())
#     encrypted_refresh_token = cipher.encrypt(token_info["refresh_token"].encode())

#     # Store encrypted tokens in session
#     session["token_info"] = {
#         "access_token": encrypted_access_token,
#         "refresh_token": encrypted_refresh_token,
#         "expires_in": token_info["expires_in"],
#     }

#     print("\nsession[token_info] = ", session["token_info"], "\n")

#     # Store encrypted tokens in database
#     #    token = Token(access_token=encrypted_access_token, refresh_token=encrypted_refresh_token)
#     #    db.session.add(token)
#     #    db.session.commit()

#     return redirect(REACT_HOMEPAGE_URL)


@app.route("/logged")
def logged():
    is_session = "spotify_token" in session
    response = make_response({"authenticated": is_session})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    
    # User is authenticated, return authenticated status
    return response, 200
    
    # access_token = sp_oauth.get_cached_token()
    # print("\nsession[token_info] (logged) = ", session.get("spotify_token"), "\n")
    # print("\n\nACCESS TOKEN = ", access_token, "\n\n")


@app.route("/refresh")
def post():
    sp_oauth = create_sp_oauth()
    if "token_info" not in session:
        return redirect(url_for("login"))

    # Check if token is expired or about to expire
    token_info = session["token_info"]

    access_token = cipher.decrypt(token_info["access_token"]).decode()
    if not access_token or sp_oauth.is_token_expired(token_info):
        refresh_access_token()
       

    return make_response(jsonify({"access_token":token_info["access_token"]}), 200)



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
