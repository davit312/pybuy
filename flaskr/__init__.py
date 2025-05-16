from flask import Flask
from flask_login import login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'example_shop_secret_key'
    
    from .shop import shop_bp
    app.register_blueprint(shop_bp, url_prefix='/')

    return app

