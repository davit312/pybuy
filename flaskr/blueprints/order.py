from flask import Blueprint, request, render_template, make_response
from flask_login import current_user, login_required

from flaskr.models import Product, OrderRecord
from flaskr import db

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders')
@login_required
def user_orders():
    orders = db.session.query(OrderRecord).filter_by(
        user_id=current_user.id,
        is_ordered=True
    ).all()

    return render_template('pages/user_orders.html', user=current_user, orders=orders)

@order_bp.route('/order/submit', methods=['POST'])
@login_required
def submit_order():

    request_data = request.get_json()
    order = db.session.query(OrderRecord).get(request_data['order_id'])

    if not order:
        return make_response('No items in basket', 400)

    if request_data.get('pay_now'):
        order.is_paid = True

    order.is_ordered = True
    db.session.add(order)
    db.session.commit()

    return make_response('Order submitted successfully', 200)



@order_bp.route('/order/send', methods=['POST'])
@login_required
def send_order():

    request_data = request.get_json()
    order = db.session.query(OrderRecord).get(request_data['order_id'])

    if not order:
        return make_response('No items in basket', 400)

    order.is_sent = True
    db.session.add(order)
    db.session.commit()
    return make_response('Order sent successfully', 200)


@order_bp.route('/order/receive', methods=['POST'])
@login_required
def receive_order():

    request_data = request.get_json()
    order = db.session.query(OrderRecord).get(request_data['order_id'])

    if not order:
        return make_response('No items in basket', 400)
    
    if not order.is_sent:
        return make_response('Order not sent', 400)
    
    order.is_delivered = True
    db.session.add(order)
    db.session.commit()
    return make_response('Order received successfully', 200)

