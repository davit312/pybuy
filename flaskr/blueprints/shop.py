from flask import Blueprint, render_template, make_response
from flask_login import current_user, login_required

from flaskr.models import Product, OrderRecord
from flaskr import db

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('pages/index.html', user=current_user, products=products)


@shop_bp.route('/basket/add/<int:product_id>/<int:quantity>', methods=['POST'])
@login_required
def add_to_basket(product_id, quantity):
    product = db.session.query(Product).filter_by(id=product_id).first()

    stock_quantity = product.in_stock 
    if product:
        existing_order = db.session.query(OrderRecord).filter_by(
            user_id=current_user.id,
            product_id=product.id,
            is_ordered=False
        ).first()
        if existing_order is not None:
            return make_response('Product already in basket', 400)
        order = OrderRecord(
            user_id=current_user.id,
            product_id=product.id,
            quantity=quantity,
            is_ordered=False
        )
        new_stock_quantity = stock_quantity - quantity

        if new_stock_quantity < 0:
            return make_response('Not enough stock', 400)

        product.in_stock = new_stock_quantity

        db.session.add(order)
        db.session.add(product)

        db.session.commit()

    return make_response('Product added to basket', 200)

@shop_bp.route('/basket/update/<int:order_id>/<int:quantity>', methods=['POST'])
@login_required
def update_basket_item(order_id, quantity):
    order = db.session.query(OrderRecord).filter_by(id=order_id).first()
    product = db.session.query(Product).filter_by(id=order.product_id).first()
    if quantity <= 0:
        return make_response('Invalid quantity', 400)

    new_stock_quantity = (product.in_stock + order.quantity) - quantity

    if new_stock_quantity < 0:
        return make_response('Not enough stock', 400)

    product.in_stock = new_stock_quantity
    order.quantity = quantity

    db.session.add(order)
    db.session.add(product)

    db.session.commit()

    return make_response('Basket item updated', 200)

@shop_bp.route('/basket/delete/<int:order_id>', methods=['POST'])
@login_required
def remove_from_basket(order_id):
    order = db.session.query(OrderRecord).get(order_id)
    product = db.session.query(Product).get(order.product_id)

    product.in_stock += order.quantity
    db.session.add(product)

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
