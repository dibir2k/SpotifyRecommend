import os
from dotenv import load_dotenv
import json
import logging

from spotipy.oauth2 import SpotifyOAuth
from spotipy import CacheHandler

import redis
from redis import RedisError

from flask import current_app

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

logger = logging.getLogger(__name__)


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

# Spotipy oauth
def create_sp_oauth():
    r = redis.Redis(host='redis')
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://localhost:80/login",
        scope="user-read-recently-played user-top-read playlist-read-private playlist-modify-private user-read-private",
        cache_handler=RedisCacheHandler(r)
    )
    return r, sp_oauth