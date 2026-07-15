from datetime import date
from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, Item, Order, OrderItem, db
from . import orders_bp
from .schemas import (order_schema, orders_schema, create_order_schema, receipt_schema)


def build_receipt(order):
    """Build a receipt dictionary for an existing order."""

    items = []
    total = 0

    for order_item in order.order_items:
        subtotal = order_item.quantity * order_item.item.price
        total += subtotal

        items.append({
            "item": order_item.item.item_name,
            "quantity": order_item.quantity,
            "price": order_item.item.price,
            "subtotal": subtotal
        })

    return {
        "order_id": order.id,
        "customer_id": order.customer_id,
        "order_date": order.order_date,
        "items": items,
        "total": total
    }


# CREATE ORDER
@orders_bp.route("/", methods=["POST"])
def create_order():
    try:
        order_data = create_order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    customer = db.session.get(Customer, order_data["customer_id"])

    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    try:
        new_order = Order(
            customer_id=order_data["customer_id"],
            order_date=date.today()
        )

        db.session.add(new_order)

        # Generates new_order.id without permanently committing yet
        db.session.flush()

        for item_data in order_data["item_quantity"]:
            item = db.session.get(Item, item_data["item_id"])

            if not item:
                db.session.rollback()

                return jsonify({
                    "message": (
                        f"Item with ID {item_data['item_id']} not found"
                    )
                }), 404

            order_item = OrderItem(
                order_id=new_order.id,
                item_id=item_data["item_id"],
                quantity=item_data["item_quantity"]
            )

            db.session.add(order_item)

        db.session.commit()

    except Exception:
        db.session.rollback()
        return jsonify({"message": "Unable to create order"}), 500

    receipt = build_receipt(new_order)

    return receipt_schema.jsonify(receipt), 201


# GET ALL ORDERS
@orders_bp.route("/", methods=["GET"])
def get_orders():
    query = select(Order)
    orders = db.session.execute(query).scalars().all()

    return orders_schema.jsonify(orders), 200


# GET ORDER BY ID
@orders_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({"message": "Order not found"}), 404

    return order_schema.jsonify(order), 200


# GET RECEIPT BY ORDER ID
@orders_bp.route("/<int:order_id>/receipt", methods=["GET"])
def get_order_receipt(order_id):
    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({"message": "Order not found"}), 404

    receipt = build_receipt(order)

    return receipt_schema.jsonify(receipt), 200


# DELETE ORDER
@orders_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({"message": "Order not found"}), 404

    try:
        # Delete associated OrderItem records first unless the model
        # relationship is configured with delete cascade.
        for order_item in order.order_items:
            db.session.delete(order_item)

        db.session.delete(order)
        db.session.commit()

    except Exception:
        db.session.rollback()
        return jsonify({"message": "Unable to delete order"}), 500

    return jsonify({
        "message": f"Order {order_id} successfully deleted"
    }), 200