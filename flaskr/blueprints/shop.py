from flask import Blueprint, render_template
from flask_login import current_user

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/')
def home():
    return render_template('pages/index.html', user=current_user)
