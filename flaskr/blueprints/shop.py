from flask import Blueprint, render_template
from flask_login import current_user

from flaskr.models import Product
from flaskr import db

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('pages/index.html', user=current_user, products=products)
