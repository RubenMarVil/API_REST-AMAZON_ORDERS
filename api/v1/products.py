# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, abort, make_response, request

class Product:
    def __init__(self, ID, name, price, supplier, rate):
        self.ID = ID
        self.name = name
        self.price = price
        self.supplier = supplier
        self.rate = rate

##############################################################################
# DATA
products_list = []
##############################################################################

products_api = Blueprint('products_api', __name__)

# Get all products
@products_api.route('/v1/products/', methods=['GET'])
def getProducts():
    return jsonify({'PRODUCTS': products_list}), 200

# Get one product from his ID
@products_api.route('/v1/products/<int:product_id>/', methods=['GET'])
def getOneProduct(product_id):
    for product in products_list:
        if product.ID == product_id:
            return jsonify({'PRODUCT': product}), 200
    abort(404)

# Create one product
@products_api.route('/v1/products/', methods=['POST'])
def createProduct():
    if not request.json or not 'ID' in request.json:
        abort(404)
    ID = request.json.get('ID')
    name = request.json.get('name')
    price = request.json.get('price')
    supplier = request.json.get('supplier')
    rate = request.json.get('rate')
    new_product = Product(ID, name, price, supplier, rate)
    products_list.append(new_product)
    return jsonify({'PRODUCT-CREATED': new_product}), 201

# Edit one product
@products_api.route('/v1/products/<int:product_id>/', methods=['PUT'])
def editProduct(product_id):
    if request.json:
        for product in products_list:
            if product.ID == product_id:
                if 'name' in request.json:
                    product.name = request.json.get('name')
                if 'price' in request.json:
                    product.price = request.json.get('price')
                if 'supplier' in request.json:
                    product.supplier = request.json.get('supplier')
                if 'rate' in request.json:
                    product.rate = request.json.get('rate')
                return jsonify({'PRODUCT-EDITED': product}), 201
        abort(404)

# Delete one product
@products_api.route('/v1/products/<int:product_id>/', methods=['DELETE'])
def deleteProduct(product_id):
    for product in products_list:
        if product.ID == product_id:
            products_list.remove(product)
            return jsonify({'PRODUCTS': products_list}), 200

# 404 errors handle
@products_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'ERROR': 'Not found'}), 404)