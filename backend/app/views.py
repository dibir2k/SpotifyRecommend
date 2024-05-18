from uuid import uuid4
import json

from flask import (
    jsonify,
    request,
    Blueprint,
    current_app
)
import redis

from spotipy import Spotify
from .spoauth import create_sp_oauth, RedisCacheHandler
from . import utils


main = Blueprint('main', __name__)

r = redis.Redis(host='redis')
sp_oauth = create_sp_oauth(r)

@main.route("/")
def index():
    return main.send_static_file("index.html")

#Get auth url
@main.route("/api/authurl")
def auth_url():
    auth_url = sp_oauth.get_authorize_url()

    return jsonify({"AuthUrl" : auth_url}), 200

#Login route
@main.route("/api/login", methods=["POST"])
def login():

    user_id = uuid4().hex

    if request.args.get("code"):
        code = request.args.get("code")

        try:
            cache_handler = RedisCacheHandler(r, user_id)
            sp_oauth.cache_handler = cache_handler
            token_info = sp_oauth.get_access_token(code, check_cache=True)
        except:
            print("\n\n ******** EXCEPTION OCCURRED ********\n\n")
            return jsonify({"id":""}), 502
        else:            
            response = jsonify({"id" : user_id}), 200
            return response
        
    else:
        return jsonify({"Error":"Failed to authenticate"}), 500
            

# Logout route
@main.route("/api/logout", methods = ["POST"])
def logout():
    id = request.headers.get('Authorization')
    r.delete(id)
    print(r.keys())

    return jsonify({"Status":"OK"}), 200


@main.route("/api/logged")
def logged():
    id = request.headers.get("Authorization")
    response = jsonify({"Authenticated":r.exists(id)}), 200
    return response


def verify_request():
    # Check if user is authenticated
    headers = request.headers
    id = headers.get("Authorization")
    token_info = json.loads(r.get(id).decode('utf-8'))
    
    if not token_info:
        return jsonify({"message" : "Forbidden access"}), 401

    if sp_oauth.is_token_expired(token_info):
        refresh_token = token_info["refresh_token"]
        token_info = sp_oauth.refresh_access_token(refresh_token)
        r.set(id, token_info)

    access_token = token_info['access_token']

    return access_token
    
@main.route("/api/recommendations/recently-played-list")
def recently_played_list():
    headers = request.headers
    id = headers.get("Authorization")
    token_info = json.loads(r.get(id).decode('utf-8'))
    
    if not token_info:
        return jsonify({"message" : "Forbidden access"}), 401

    if sp_oauth.is_token_expired(token_info):
        refresh_token = token_info["refresh_token"]
        token_info = sp_oauth.refresh_access_token(refresh_token)
        r.set(id, token_info)

    access_token = token_info['access_token']

    # Initialize Spotipy with the access token
    sp = Spotify(auth=access_token)

    rp_json = jsonify(utils.get_recently_played_list(sp))

    return rp_json


@main.route("/api/recommendations/recently-played")
def recently_played_recommendations():
    headers = request.headers
    id = headers.get("Authorization")
    token_info = json.loads(r.get(id).decode('utf-8'))
    
    if not token_info:
        return jsonify({"message" : "Forbidden access"}), 401

    if sp_oauth.is_token_expired(token_info):
        refresh_token = token_info["refresh_token"]
        token_info = sp_oauth.refresh_access_token(refresh_token)
        r.set(id, token_info)

    access_token = token_info['access_token']

    # Initialize Spotipy with the access token
    sp = Spotify(auth=access_token)

    recommended_json = jsonify(utils.recommended(sp, 50, mode="rp"))
    return recommended_json

@main.route("/api/recommendations/top-tracks-list")
def top_tracks_list():
    headers = request.headers
    id = headers.get("Authorization")
    token_info = json.loads(r.get(id).decode('utf-8'))
    
    if not token_info:
        return jsonify({"message" : "Forbidden access"}), 401

    if sp_oauth.is_token_expired(token_info):
        refresh_token = token_info["refresh_token"]
        token_info = sp_oauth.refresh_access_token(refresh_token)
        r.set(id, token_info)

    access_token = token_info['access_token']

    # Initialize Spotipy with the access token
    sp = Spotify(auth=access_token)

    tt_json = jsonify(utils.get_top_tracks_list(sp))

    return tt_json


@main.route("/api/recommendations/top-tracks")
def top_tracks_recommendations():
    headers = request.headers
    id = headers.get("Authorization")
    token_info = json.loads(r.get(id).decode('utf-8'))
    
    if not token_info:
        return jsonify({"message" : "Forbidden access"}), 401

    if sp_oauth.is_token_expired(token_info):
        refresh_token = token_info["refresh_token"]
        token_info = sp_oauth.refresh_access_token(refresh_token)
        r.set(id, token_info)

    access_token = token_info['access_token']

    # Initialize Spotipy with the access token
    sp = Spotify(auth=access_token)

    recommended_json = jsonify(utils.recommended(sp, 50, mode="tt"))
    return recommended_json    


@main.route("/api/recommendations/my-playlists")
def my_playlists():
    headers = request.headers
    id = headers.get("Authorization")
    token_info = json.loads(r.get(id).decode('utf-8'))
    
    if not token_info:
        return jsonify({"message" : "Forbidden access"}), 401

    if sp_oauth.is_token_expired(token_info):
        refresh_token = token_info["refresh_token"]
        token_info = sp_oauth.refresh_access_token(refresh_token)
        r.set(id, token_info)

    access_token = token_info['access_token']

    # Initialize Spotipy with the access token
    sp = Spotify(auth=access_token)

    # Fetch recently played tracks
    user_playlists = sp.current_user_playlists(limit = 50, offset=0)
    
    playlist_items = []
    keys = ["playlist_id", "playlist_name", "image_url"]
    for playlist in user_playlists['items']:
        playlist_id = playlist['id']
        playlist_name = playlist['name']
        playlist_image_url = playlist['images'][0]['url'] if playlist['images'] else '' 
        playlist_items.append(dict(zip(keys, [playlist_id, playlist_name, playlist_image_url])))

    return jsonify(playlist_items)


@main.route('/api/recommendations/playlist/playlist-data')
def get_playlist_items():
    headers = request.headers
    id = headers.get("Authorization")
    playlist_id = headers.get("Playlist-id")
    token_info = json.loads(r.get(id).decode('utf-8'))
    
    if not token_info:
        return jsonify({"message" : "Forbidden access"}), 401

    if sp_oauth.is_token_expired(token_info):
        refresh_token = token_info["refresh_token"]
        token_info = sp_oauth.refresh_access_token(refresh_token)
        r.set(id, token_info)

    access_token = token_info['access_token']

    # Initialize Spotipy with the access token
    sp = Spotify(auth=access_token)
    playlist_tracks = sp.playlist(playlist_id)["tracks"]["items"]

    tracks = []

    for track in playlist_tracks:
        track = track["track"]
        track_name = track["name"]
        track_id = track["id"]
        artist_name = ""
        n_artists = len(track["artists"])
        for i, artist in enumerate(track["artists"]):
            artist_name = artist_name.join(artist["name"])
            if i < n_artists -1:
                artist_name.join(", ")

        duration = utils.ms_to_string(track["duration_ms"])
        album_name = track["album"]["name"]
        image = track["album"]["images"][2]["url"]

        tracks.append({"track_name":track_name, "artist_name":artist_name, "track_id":track_id, 
                      "duration":duration, "album_name":album_name, "image":image})

    tracks_json = jsonify(tracks)

    return tracks_json, 200



@main.route('/api/recommendations/playlist/<playlist_id>')
def my_playlist_recommendations(playlist_id):
    headers = request.headers
    id = headers.get("Authorization")
    token_info = json.loads(r.get(id).decode('utf-8'))
    
    if not token_info:
        return jsonify({"message" : "Forbidden access"}), 401

    if sp_oauth.is_token_expired(token_info):
        refresh_token = token_info["refresh_token"]
        token_info = sp_oauth.refresh_access_token(refresh_token)
        r.set(id, token_info)

    access_token = token_info['access_token']

    # Initialize Spotipy with the access token
    sp = Spotify(auth=access_token)
    username = sp.current_user()["id"]

    recommended_json = jsonify(utils.recommended(sp, limit=50, mode="in", track_name=playlist_id, username=username))

    return recommended_json


@main.route('/api/recommendations/track', methods = ["POST"])
def track_recommendations():
    headers = request.headers
    id = headers.get("Authorization")
    token_info = json.loads(r.get(id).decode('utf-8'))
    
    if not token_info:
        return jsonify({"message" : "Forbidden access"}), 401

    if sp_oauth.is_token_expired(token_info):
        refresh_token = token_info["refresh_token"]
        token_info = sp_oauth.refresh_access_token(refresh_token)
        r.set(id, token_info)

    access_token = token_info['access_token']

    track_name = request.json.get("trackName")
    artist_name = request.json.get("artistName")

    # Initialize Spotipy with the access token
    sp = Spotify(auth=access_token)
    username = sp.current_user()["id"]

    recommended_json = jsonify(utils.recommended(sp, limit=200, mode="in", track_name=track_name, artist_name=artist_name))

    return recommended_json, 200


@main.route('/api/recommendations/playlist', methods = ["POST"])
def playlist_recommendations():
    headers = request.headers
    id = headers.get("Authorization")
    token_info = json.loads(r.get(id).decode('utf-8'))

    if not token_info:
        return jsonify({"message" : "Forbidden access"}), 401

    if sp_oauth.is_token_expired(token_info):
        refresh_token = token_info["refresh_token"]
        token_info = sp_oauth.refresh_access_token(refresh_token)
        r.set(id, token_info)

    access_token = token_info['access_token']

    playlist_url = request.json.get("url")

    # Initialize Spotipy with the access token
    sp = Spotify(auth=access_token)
    username = sp.current_user()["id"]

    recommended_json = jsonify(utils.recommended(sp, limit=50, mode="in", track_name=playlist_url, username=username))

    return recommended_json, 200