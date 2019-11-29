# -*- coding: utf-8 -*

from api.v1.addresses import addresses_list
from api.v1.products import products_list, Product

from flask import Blueprint, jsonify, abort, make_response, request

class Order:
    def __init__(self, ID, order_date, delivery_date, price, address, products):
        self.ID = ID
        self.order_date = order_date
        self.delivery_date = delivery_date
        self.price = price
        self.address = address
        self.products = products

##############################################################################
# DATA
orders_list = [Order(1, '23-04-2019', '04-05-2019', 44.48, addresses_list[2], [products_list[1], products_list[2]]),
Order(2, '14-05-2019', '21-05-2019', 99.97, addresses_list[1], [products_list[0], products_list[3], products_list[3]])]
##############################################################################

orders_api = Blueprint('orders_api', __name__)

# Get all orders
@orders_api.route('/v1/orders/', methods=['GET'])
def getOrders():
    return jsonify({'ORDERS': orders_list}), 200

# Get one order from his ID
@orders_api.route('/v1/orders/<int:order_id>/', methods=['GET'])
def getOneOrder(order_id):
    for order in orders_list:
        if order.ID == order_id:
            return jsonify({'ORDER': order}), 200
    abort(404)

# Edit one order
@orders_api.route('/v1/orders/<int:order_id>/', methods=['PUT'])
def editOrder(order_id):
    if request.json:
        for order in orders_list:
            if order.ID == order_id:
                if 'delivery_date' in request.json:
                    order.delivery_date = request.json.get('delivery_date')
                return jsonify({'ORDER-EDITED': order}), 201
        abort(404)
    abort(400)

# Delete one order
@orders_api.route('/v1/orders/<int:order_id>/', methods=['DELETE'])
def deleteOrder(order_id):
    for order in orders_list:
        if order.ID == order_id:
            orders_list.remove(order)
            return jsonify({'ORDERS': orders_list}), 200
    abort(404)

# Get address of one order
@orders_api.route('/v1/orders/<int:order_id>/address/')
def getAddressOfOrder(order_id):
    for order in orders_list:
        if order.ID == order_id:
            return jsonify({'ADDRESS': order.address}), 200
    abort(404)

# Get all products of one order
@orders_api.route('/v1/orders/<int:order_id>/products/', methods=['GET'])
def getProductsOfOrder(order_id):
    for order in orders_list:
        if order.ID == order_id:
            return jsonify({'PRODUCTS': order.products}), 200
    abort(404)

# Get one product of one order
@orders_api.route('/v1/orders/<int:order_id>/products/<int:product_id>/', methods=['GET'])
def getOneProductOfOrder(order_id, product_id):
    for order in orders_list:
        if order.ID == order_id:
            for product in order.products:
                if product.ID == product_id:
                    return jsonify({'PRODUCT': product}), 200
    abort(404)

# Add one product to one order
@orders_api.route('/v1/orders/<int:order_id>/products/', methods=['POST'])
def addOneProductToOneOrder(order_id):
    if request.json:
        for order in orders_list:
            if order.ID == order_id:
                ID = request.json.get('ID')
                for product in products_list:
                    if product.ID == ID:
                        order.products.append(product)
                        order.price += product.price
                        return jsonify({'PRODUCTS': order.products}), 201
        abort(404)
    abort(400)

# Delete one product of one order
@orders_api.route('/v1/orders/<int:order_id>/products/<int:product_id>/', methods=['DELETE'])
def deleteOneProductOfOneOrder(order_id, product_id):
    for order in orders_list:
        if order.ID == order_id:
            for product in products_list:
                if product.ID == product_id:
                    order.products.remove(product)
                    order.price -= product.price
                    return jsonify({'PRODUCTS': order.products}), 200
    abort(404)

# 404 errors handle
@orders_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'ERROR': 'Not found'}), 404)

# 400 errors handle
@orders_api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'ERROR': 'Bad Request'}),400)