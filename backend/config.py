import os 
import redis 

class AppConfig:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = True
    SESSION_COOKIE_HTTPONLY = True  # Make the session cookie HttpOnly
    SESSION_COOKIE_SAMESITE = 'None'  # Set SameSite attribute to 'None' for cross-origin requests
    #SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
