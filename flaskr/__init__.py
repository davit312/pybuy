from flask import Flask
from flask_login import login_manager
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'example_shop_secret_key'
    
    from .blueprints.shop import shop_bp
    from .blueprints.auth import auth_bp

    app.register_blueprint(shop_bp)
    app.register_blueprint(auth_bp)

    return app

