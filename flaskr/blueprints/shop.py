from flask import Blueprint, render_template

shop_bp = Blueprint('admin', __name__)

@shop_bp.route('/')
def admin_dashboard():
    return render_template('pages/index.html')
