# rsa_tool/app.py
"""
RSA Cryptography Tool - Main Application
Entry point for the Flask web application
"""
from flask import Flask
from controllers import register_routes
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['DEBUG'] = True
    app.config['HOST'] = '127.0.0.1'
    app.config['PORT'] = 5000
    
    # Register all routes
    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )