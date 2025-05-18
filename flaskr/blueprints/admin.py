from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

import os.path
from time import time

from flaskr.models import Product
from flaskr import db

admin_bp = Blueprint('admin', __name__, url_prefix='/')

@admin_bp.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if request.method == 'POST':
        product_name = request.form.get('name')
        product_price = request.form.get('price')
        product_in_stock = int(request.form.get('in_stock'))
        product_description = request.form.get('description')
        product_image = request.files.get('image')

        if not product_name or not product_price or not product_description:
            flash('All fields are required!', 'danger')
            return redirect(url_for('admin.new_product'))
        
        if product_in_stock < 0:
            flash('Product count is invalid', 'error')
            return redirect(url_for('admin.new_product'))

        if product_image and product_image.filename != '':
            filename = str(time()).replace('.', '') + os.path.splitext(product_image.filename)[1]
            product_image.save(os.path.join('flaskr/static/uploads', filename))

        new_product = Product(
            name=product_name,
            price=float(product_price),
            in_stock=int(product_in_stock),
            description=product_description,
            image=filename if product_image else None
        )

        db.session.add(new_product)
        db.session.commit()

        flash('Product created successfully!', 'success')
        return redirect(url_for('admin.new_product'))

    return render_template('pages/product-form.html', user=current_user)