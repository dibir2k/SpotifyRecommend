from flask import Flask
from flask_cors import CORS
import logging

from .config import AppConfig

def create_app():
    app = Flask(__name__, static_url_path="/")
    app.config.from_object(AppConfig)

    # Enable CORS
    CORS(app, origins=['http://spotify-recommend-frontend:80'], supports_credentials=True)
    
    # Configure logging
    logging.basicConfig(filename='./app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

    # Register blueprints
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app