import os 
import redis 

class AppConfig:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = True
    SESSION_COOKIE_HTTPONLY = True  
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    QDRANT_HOST = 'qdrant'
    QDRANT_PORT = 6334
    QDRANT_TIMEOUT = 10
