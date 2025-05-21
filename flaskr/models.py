from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(180), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    is_admin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(40))
    price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)

class OrderRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id', ondelete="CASCADE"), nullable=False)
    is_ordered = db.Column(db.Boolean, default=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=func.now())
    is_paid = db.Column(db.Boolean, default=False)
    is_sent = db.Column(db.Boolean, default=False)
    is_delivered = db.Column(db.Boolean, default=False)
    product = db.relationship('Product', backref='OrderRecord', passive_deletes=True)
