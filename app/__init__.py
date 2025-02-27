from flask import Flask
from flask_cors import CORS
from app.extensions import register_extensions
from app.api import api_bp

def create_app(config_object=None):
    """
    Application factory pattern
    """
    app = Flask(__name__)
   
    if config_object:
        app.config.from_object(config_object)
   
    register_extensions(app)
   
    CORS(app, 
     origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://instaclean.vercel.app", "https://instagram-cleanup-tool-api.vercel.app"],
     supports_credentials=True)
   
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
   
    return app