# -*- coding: utf-8 -*

from api.v1.addresses import addresses_list, Address

from flask import Blueprint, jsonify, abort, make_response, request

class Order:
    def __init__(self, ID, order_date, delivery_date, price, address):
        self.ID = ID
        self.order_date = order_date
        self.delivery_date = delivery_date
        self.price = price
        self.address = address

##############################################################################
# DATA
orders_list = []
##############################################################################

orders_api = Blueprint('orders_api', __name__)

# Get all orders
@orders_api.route('/v1/orders/', methods=['GET'])
def getOrders():
    return jsonify({'ORDERS': orders_list}), 200

# Get one order from his ID
@orders_api.route('/v1/orders/<int:order_id>', methods=['GET'])
def getOneOrder(order_id):
    for order in orders_list:
        if order.ID == order_id:
            return jsonify({'ORDER': order}), 200
    abort(404)

# Create one order
@orders_api.route('/v1/orders/', methods=['POST'])
def createOrder():
    if not request.json or not 'ID' in request.json:
        abort(404)
    ID = request.json.get('ID')
    order_date = request.json.get('order_date')
    delivery_date = request.json.get('delivery_date')
    price = request.json.get('price')
    address = request.json.get('address')
    new_order = Order(ID, order_date, delivery_date, price, address)
    orders_list.append(new_order)
    return jsonify({'ORDER-CREATED': new_order}), 201

# Edit one order
@orders_api.route('/v1/orders/<int:order_id>/', methods=['PUT'])
def editOrder(order_id):
    if request.json:
        for order in orders_list:
            if order.ID == order_id:
                if 'order_date' in request.json:
                    order.order_date = request.json.get('order_date')
                if 'delivery_date' in request.json:
                    order.delivery_date = request.json.get('delivery_date')
                if 'price' in request.json:
                    order.price = request.json.get('price')
                if 'address' in request.json:
                    order.address = request.json.get('address')
                return jsonify({'ORDER-EDITED': order}), 201
        abort(404)

# Delete one order
@orders_api.route('/v1/orders/<int:order_id>/', methods=['DELETE'])
def deleteOrder(order_id):
    for order in orders_list:
        if order.ID == order_id:
            orders_list.remove(order)
            return jsonify({'ORDERS': orders_list}), 200

# Get address of one order
@orders_api.route('/v1/orders/<int:order_id>/address/')
def getAddressOfOrder(order_id):
    for order in orders_list:
        if order.ID == order_id:
            return jsonify({'ADDRESS': order.address})
    abort(404)

# Create address to one order

# 404 errors handle
@orders_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'ERROR': 'Not found'}), 404)