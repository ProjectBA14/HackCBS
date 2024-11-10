from flask import Flask
from .routes import configure_routes
import firebase_admin
from firebase_admin import credentials, firestore

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Replace with a secure, randomly generated key

    # Firebase setup
    if not firebase_admin._apps:  # Prevent re-initialization if already initialized
        cred = credentials.Certificate('firebase/firebase_config.json')
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()  # Ensure `db` is used or imported elsewhere as needed

    # Register routes
    configure_routes(app)
    
    return app
