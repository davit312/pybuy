from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

import os.path
from time import time

from flaskr.models import User
from flaskr import db

admin_bp = Blueprint('admin', __name__, url_prefix='/')

@admin_bp.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if request.method == 'POST':
        product_name = request.form.get('name')
        product_price = request.form.get('price')
        product_description = request.form.get('description')
        product_image = request.files.get('image')

        if not product_name or not product_price or not product_description:
            flash('All fields are required!', 'danger')
            return redirect(url_for('admin.new_product'))

        if product_image and product_image.filename != '':
            filename = str(time()).replace('.', '') + os.path.splitext(product_image.filename)[1]
            product_image.save(os.path.join('flaskr/static/uploads', filename))

        flash('Product created successfully!', 'success')
        return redirect(url_for('admin.new_product'))

    return render_template('pages/product-form.html', user=current_user)