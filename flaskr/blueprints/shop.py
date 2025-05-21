from flask import Blueprint, render_template, make_response
from flask_login import current_user, login_required

from flaskr.models import Product, OrderRecord
from flaskr import db

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('pages/index.html', user=current_user, products=products)


@shop_bp.route('/basket/put/<int:product_id>/<int:quantity>', methods=['POST'])
@login_required
def put_to_basket(product_id, quantity):
    product = db.session.query(Product).get(product_id)
    if product:
        new_stock_quantity = product.in_stock - quantity
        if new_stock_quantity >= 0:
            product.in_stock = new_stock_quantity
            existing_order = db.session.query(OrderRecord).filter_by(
                user_id=current_user.id,
                product_id=product.id,
                is_ordered=False
            ).first()
            if existing_order:
                order = existing_order
            else:
                order = OrderRecord(
                    user_id=current_user.id,
                    product_id=product.id,
                    quantity=quantity,
                    is_ordered=False
                )
            db.session.add(order)
            db.session.commit()
        else:
            return make_response('Product out of stock', 400)
    return make_response('Product added to basket', 200)

@shop_bp.route('/basket/delete/<int:product_id>', methods=['GET'])
@login_required
def remove_from_basket(product_id, quantity):
    order = db.session.query(OrderRecord).filter_by(
        user_id=current_user.id,
        product_id=product_id,
        is_ordered=False
    )
    product = db.session.query(Product).get(product_id)
    product.in_stock += quantity

    if not order:
        return make_response('Product not in basket', 400)

    db.session.delete(order)
    db.session.commit()
    return make_response('Product removed from basket', 200)

@shop_bp.route('/basket')
@login_required
def basket():
    items = db.session.query(OrderRecord).filter_by(
        user_id=current_user.id,
        is_ordered=False
    ).all()

    return render_template('pages/basket.html', user=current_user, items=items)

