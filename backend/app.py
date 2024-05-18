# from flask_cors import CORS
# from flask_session import Session

# from flask import (
#     Flask,
#     jsonify,
#     request,
#     Blueprint
# )

# import redis
# from redis import RedisError

# from spotipy import Spotify, CacheHandler
# from spotipy.oauth2 import SpotifyOAuth

# from uuid import uuid4
# import os
# import json
# from cryptography.fernet import Fernet
# import logging

# from dotenv import load_dotenv

# import backend.app.utils as utils
# from config import AppConfig

# app = Flask(__name__, static_url_path="/", static_folder="./client/build")
# app.config.from_object(AppConfig)

# server_session = Session(app)

# CORS(app, origins=['http://spotify-recommend-frontend:80'], supports_credentials=True)

# # Configure logging
# logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

# logger = logging.getLogger(__name__)

# class RedisCacheHandler(CacheHandler):
#     """
#     A cache handler that stores the token info in the Redis.
#     """

#     def __init__(self, redis, key=None):
#         """
#         Parameters:
#             * redis: Redis object provided by redis-py library
#             (https://github.com/redis/redis-py)
#             * key: May be supplied, will otherwise be generated
#                    (takes precedence over `token_info`)
#         """
#         self.redis = redis
#         self.key = key if key else 'token_info'

#     def get_cached_token(self):
#         token_info = None
#         try:
#             token_info = self.redis.get(self.key)
#             if token_info:
#                 return json.loads(token_info)
#         except RedisError as e:
#             logger.warning('Error getting token from cache: ' + str(e))

#         return token_info

#     def save_token_to_cache(self, token_info):
#         try:
#             self.redis.set(self.key, json.dumps(token_info))
#         except RedisError as e:
#             logger.warning('Error saving token to cache: ' + str(e))

# r = redis.Redis(host='redis')

# load_dotenv()

# CLIENT_ID = os.getenv('CLIENT_ID')
# CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# # Spotipy oauth
# def create_sp_oauth():
#     sp_oauth = SpotifyOAuth(
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         redirect_uri="http://localhost:80/login",
#         scope="user-read-recently-played user-top-read playlist-read-private playlist-modify-private user-read-private",
#         cache_handler=RedisCacheHandler(r)
#     )
#     return sp_oauth

# sp_oauth = create_sp_oauth()

#api_bp = Blueprint("api", __name__, url_prefix="/api")

# @app.route("/")
# def index():
#     return app.send_static_file("index.html")

# #Get auth url
# @app.route("/api/authurl")
# def auth_url():
#     auth_url = sp_oauth.get_authorize_url()

#     return jsonify({"AuthUrl" : auth_url}), 200

# #Login route
# @app.route("/api/login", methods=["POST"])
# def login():

#     user_id = uuid4().hex

#     if request.args.get("code"):
#         code = request.args.get("code")

#         try:
#             cache_handler = RedisCacheHandler(r, user_id)
#             sp_oauth.cache_handler = cache_handler
#             token_info = sp_oauth.get_access_token(code, check_cache=True)
#         except:
#             print("\n\n ******** EXCEPTION OCCURRED ********\n\n")
#             return jsonify({"id":""}), 502
#         else:            
#             response = jsonify({"id" : user_id}), 200
#             return response
        
#     else:
#         return jsonify({"Error":"Failed to authenticate"}), 500
            
    


# # Logout route
# @app.route("/api/logout", methods = ["POST"])
# def logout():
#     id = request.headers.get('Authorization')
#     r.delete(id)
#     print(r.keys())

#     return jsonify({"Status":"OK"}), 200


# @app.route("/api/logged")
# def logged():
#     id = request.headers.get("Authorization")
#     response = jsonify({"Authenticated":r.exists(id)}), 200
#     return response


# def verify_request():
#     # Check if user is authenticated
#     headers = request.headers
#     id = headers.get("Authorization")
#     token_info = json.loads(r.get(id).decode('utf-8'))
    
#     if not token_info:
#         return jsonify({"message" : "Forbidden access"}), 401

#     if sp_oauth.is_token_expired(token_info):
#         refresh_token = token_info["refresh_token"]
#         token_info = sp_oauth.refresh_access_token(refresh_token)
#         r.set(id, token_info)

#     access_token = token_info['access_token']

#     return access_token
    
# @app.route("/api/recommendations/recently-played-list")
# def recently_played_list():
#     headers = request.headers
#     id = headers.get("Authorization")
#     token_info = json.loads(r.get(id).decode('utf-8'))
    
#     if not token_info:
#         return jsonify({"message" : "Forbidden access"}), 401

#     if sp_oauth.is_token_expired(token_info):
#         refresh_token = token_info["refresh_token"]
#         token_info = sp_oauth.refresh_access_token(refresh_token)
#         r.set(id, token_info)

#     access_token = token_info['access_token']

#     # Initialize Spotipy with the access token
#     sp = Spotify(auth=access_token)

#     rp_json = jsonify(utils.get_recently_played_list(sp))

#     return rp_json


# @app.route("/api/recommendations/recently-played")
# def recently_played_recommendations():
#     headers = request.headers
#     id = headers.get("Authorization")
#     token_info = json.loads(r.get(id).decode('utf-8'))
    
#     if not token_info:
#         return jsonify({"message" : "Forbidden access"}), 401

#     if sp_oauth.is_token_expired(token_info):
#         refresh_token = token_info["refresh_token"]
#         token_info = sp_oauth.refresh_access_token(refresh_token)
#         r.set(id, token_info)

#     access_token = token_info['access_token']

#     # Initialize Spotipy with the access token
#     sp = Spotify(auth=access_token)

#     recommended_json = jsonify(utils.recommended(sp, 50, mode="rp"))
#     return recommended_json

# @app.route("/api/recommendations/top-tracks-list")
# def top_tracks_list():
#     headers = request.headers
#     id = headers.get("Authorization")
#     token_info = json.loads(r.get(id).decode('utf-8'))
    
#     if not token_info:
#         return jsonify({"message" : "Forbidden access"}), 401

#     if sp_oauth.is_token_expired(token_info):
#         refresh_token = token_info["refresh_token"]
#         token_info = sp_oauth.refresh_access_token(refresh_token)
#         r.set(id, token_info)

#     access_token = token_info['access_token']

#     # Initialize Spotipy with the access token
#     sp = Spotify(auth=access_token)

#     tt_json = jsonify(utils.get_top_tracks_list(sp))

#     return tt_json


# @app.route("/api/recommendations/top-tracks")
# def top_tracks_recommendations():
#     headers = request.headers
#     id = headers.get("Authorization")
#     token_info = json.loads(r.get(id).decode('utf-8'))
    
#     if not token_info:
#         return jsonify({"message" : "Forbidden access"}), 401

#     if sp_oauth.is_token_expired(token_info):
#         refresh_token = token_info["refresh_token"]
#         token_info = sp_oauth.refresh_access_token(refresh_token)
#         r.set(id, token_info)

#     access_token = token_info['access_token']

#     # Initialize Spotipy with the access token
#     sp = Spotify(auth=access_token)

#     recommended_json = jsonify(utils.recommended(sp, 50, mode="tt"))
#     return recommended_json    


# @app.route("/api/recommendations/my-playlists")
# def my_playlists():
#     headers = request.headers
#     id = headers.get("Authorization")
#     token_info = json.loads(r.get(id).decode('utf-8'))
    
#     if not token_info:
#         return jsonify({"message" : "Forbidden access"}), 401

#     if sp_oauth.is_token_expired(token_info):
#         refresh_token = token_info["refresh_token"]
#         token_info = sp_oauth.refresh_access_token(refresh_token)
#         r.set(id, token_info)

#     access_token = token_info['access_token']

#     # Initialize Spotipy with the access token
#     sp = Spotify(auth=access_token)

#     # Fetch recently played tracks
#     user_playlists = sp.current_user_playlists(limit = 50, offset=0)
    
#     playlist_items = []
#     keys = ["playlist_id", "playlist_name", "image_url"]
#     for playlist in user_playlists['items']:
#         playlist_id = playlist['id']
#         playlist_name = playlist['name']
#         playlist_image_url = playlist['images'][0]['url'] if playlist['images'] else '' 
#         playlist_items.append(dict(zip(keys, [playlist_id, playlist_name, playlist_image_url])))

#     return jsonify(playlist_items)


# @app.route('/api/recommendations/playlist/playlist-data')
# def get_playlist_items():
#     headers = request.headers
#     id = headers.get("Authorization")
#     playlist_id = headers.get("Playlist-id")
#     token_info = json.loads(r.get(id).decode('utf-8'))
    
#     if not token_info:
#         return jsonify({"message" : "Forbidden access"}), 401

#     if sp_oauth.is_token_expired(token_info):
#         refresh_token = token_info["refresh_token"]
#         token_info = sp_oauth.refresh_access_token(refresh_token)
#         r.set(id, token_info)

#     access_token = token_info['access_token']

#     # Initialize Spotipy with the access token
#     sp = Spotify(auth=access_token)
#     playlist_tracks = sp.playlist(playlist_id)["tracks"]["items"]

#     tracks = []

#     for track in playlist_tracks:
#         track = track["track"]
#         track_name = track["name"]
#         track_id = track["id"]
#         artist_name = ""
#         n_artists = len(track["artists"])
#         for i, artist in enumerate(track["artists"]):
#             artist_name = artist_name.join(artist["name"])
#             if i < n_artists -1:
#                 artist_name.join(", ")

#         duration = utils.ms_to_string(track["duration_ms"])
#         album_name = track["album"]["name"]
#         image = track["album"]["images"][2]["url"]

#         tracks.append({"track_name":track_name, "artist_name":artist_name, "track_id":track_id, 
#                       "duration":duration, "album_name":album_name, "image":image})

#     tracks_json = jsonify(tracks)

#     return tracks_json, 200



# @app.route('/api/recommendations/playlist/<playlist_id>')
# def my_playlist_recommendations(playlist_id):
#     headers = request.headers
#     id = headers.get("Authorization")
#     token_info = json.loads(r.get(id).decode('utf-8'))
    
#     if not token_info:
#         return jsonify({"message" : "Forbidden access"}), 401

#     if sp_oauth.is_token_expired(token_info):
#         refresh_token = token_info["refresh_token"]
#         token_info = sp_oauth.refresh_access_token(refresh_token)
#         r.set(id, token_info)

#     access_token = token_info['access_token']

#     # Initialize Spotipy with the access token
#     sp = Spotify(auth=access_token)
#     username = sp.current_user()["id"]

#     recommended_json = jsonify(utils.recommended(sp, limit=50, mode="in", track_name=playlist_id, username=username))

#     return recommended_json


# @app.route('/api/recommendations/track', methods = ["POST"])
# def track_recommendations():
#     headers = request.headers
#     id = headers.get("Authorization")
#     token_info = json.loads(r.get(id).decode('utf-8'))
    
#     if not token_info:
#         return jsonify({"message" : "Forbidden access"}), 401

#     if sp_oauth.is_token_expired(token_info):
#         refresh_token = token_info["refresh_token"]
#         token_info = sp_oauth.refresh_access_token(refresh_token)
#         r.set(id, token_info)

#     access_token = token_info['access_token']

#     track_name = request.json.get("trackName")
#     artist_name = request.json.get("artistName")

#     # Initialize Spotipy with the access token
#     sp = Spotify(auth=access_token)
#     username = sp.current_user()["id"]

#     recommended_json = jsonify(utils.recommended(sp, limit=200, mode="in", track_name=track_name, artist_name=artist_name))

#     return recommended_json, 200


# @app.route('/api/recommendations/playlist', methods = ["POST"])
# def playlist_recommendations():
#     headers = request.headers
#     id = headers.get("Authorization")
#     token_info = json.loads(r.get(id).decode('utf-8'))

#     if not token_info:
#         return jsonify({"message" : "Forbidden access"}), 401

#     if sp_oauth.is_token_expired(token_info):
#         refresh_token = token_info["refresh_token"]
#         token_info = sp_oauth.refresh_access_token(refresh_token)
#         r.set(id, token_info)

#     access_token = token_info['access_token']

#     playlist_url = request.json.get("url")

#     # Initialize Spotipy with the access token
#     sp = Spotify(auth=access_token)
#     username = sp.current_user()["id"]

#     recommended_json = jsonify(utils.recommended(sp, limit=50, mode="in", track_name=playlist_url, username=username))

#     return recommended_json, 200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", debug=True)
