from flask import Flask
from flask_login import login_manager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_URI = 'mysql+pymysql://shop:shop@localhost/shop'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'example_shop_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # 16MB limit

    from .blueprints.shop import shop_bp
    from .blueprints.auth import auth_bp
    from .blueprints.admin import admin_bp

    app.register_blueprint(shop_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    db.init_app(app)
    from .models import User
    with app.app_context():
        db.create_all()

    loginManager = login_manager.LoginManager()

    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    @loginManager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
