from flask import Blueprint, render_template, request, make_response,\
                    flash, redirect, url_for
from flask_login import login_required, current_user

import os.path
from time import time

from flaskr.models import Product, OrderRecord
from flaskr import db

admin_bp = Blueprint('admin', __name__, url_prefix='/')

@admin_bp.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if not current_user.is_admin:
        flash('You do not have permission to access that page.', 'error')
        return redirect(url_for('shop.home'))

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

    return render_template('pages/product-form.html', user=current_user, product=None)


@admin_bp.route('/product/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if not current_user.is_admin:
        flash('You do not have permission to access that page.', 'error')
        return redirect(url_for('shop.home'))

    product = Product.query.get(id)
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('shop.home'))

    if request.method == 'POST':
        product_name = request.form.get('name')
        product_price = request.form.get('price')
        product_in_stock = int(request.form.get('in_stock'))
        product_description = request.form.get('description')
        product_image = request.files.get('image')
        update_image = request.form.get('update_image') == 'on'

        if not product_name or not product_price or not product_description:
            flash('All fields are required!', 'danger')
            return redirect(url_for('shop.edit_product', id=id))
        
        if product_in_stock < 0:
            flash('Product count is invalid', 'error')
            return redirect(url_for('admin.edit_product', id=id))

        if update_image:
            if product_image and product_image.filename != '':
                filename = str(time()).replace('.', '') + os.path.splitext(product_image.filename)[1]
                product_image.save(os.path.join('flaskr/static/uploads', filename))
            else:
                filename = None
            os.unlink(os.path.join('flaskr/static/uploads', product.image)) if product.image else None
            product.image = filename

        product.name = product_name
        product.price = float(product_price)
        product.in_stock = int(product_in_stock)
        product.description = product_description

        db.session.commit()

        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.dashboard', id=id))
    return render_template('pages/product-form.html', user=current_user, product=product)

@admin_bp.route('/product/delete', methods=['POST'])
@login_required
def delete_product():
    if not current_user.is_admin:
        flash('You do not have permission to access that page.', 'error')
        return redirect(url_for('shop.home'))

    product_id = request.get_json().get('product_id')
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found!', 'error')
        return make_response('Product not found!', 404)

    db.session.delete(product)
    db.session.commit()

    flash('Product deleted successfully!', 'success')
    return make_response('Product deleted successfully!', 200)

@admin_bp.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access that page.', 'error')
        return redirect(url_for('shop.home'))

    return render_template('pages/admin.html', user=current_user, products=Product.query.all())

@admin_bp.route('/admin/orders', methods=['GET'])
@login_required
def order_list():
    if not current_user.is_admin:
        flash('You do not have permission to access that page.', 'error')
        return redirect(url_for('shop.home'))
    
    return render_template('pages/order_list.html', user=current_user, 
                           orders=OrderRecord.query.filter_by(is_ordered=True))