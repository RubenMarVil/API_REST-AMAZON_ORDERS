# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, abort, make_response, request

class Product:
    def __init__(self, ID, name, price, type_product, supplier, rate):
        self.ID = ID
        self.name = name
        self.price = price
        self.type_product = type_product
        self.supplier = supplier
        self.rate = rate

##############################################################################
# DATA
products_list = [Product(1, 'Razer Mamba Wireless', 79.99, 'Mouse', 'Razer', 4.0),
Product(2, 'Cable Matters Thunderbolt 3 USB C Cable Certificado de 20 Gbps', 32.99, 'Cable', 'Cable Matters', 3.5),
Product(3, 'Trust Almo', 11.49, 'Music', 'Trust', 2.2),
Product(4, 'TRIWONDER Guantes de Invierno Pantalla Táctil', 9.99, 'Clothing', 'Naturehike', 4.1),
Product(5, 'MK-Bamboo Sevilla', 16.96, 'Kitchenware', 'MK-Bamboo', 2.3)]
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
    if not request.json or not 'name' in request.json:
        abort(400)
    ID = products_list[-1].ID + 1
    name = request.json.get('name')
    price = request.json.get('price')
    type_product = request.json.get('type_product')
    supplier = request.json.get('supplier')
    new_product = Product(ID, name, price, type_product, supplier, 0.0)
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
                if 'type_product' in request.json:
                    product.type_product = request.json.get('type_product')
                if 'supplier' in request.json:
                    product.supplier = request.json.get('supplier')
                if 'rate' in request.json:
                    product.rate = request.json.get('rate')
                return jsonify({'PRODUCT-EDITED': product}), 201
        abort(404)
    abort(400)

# Delete one product
@products_api.route('/v1/products/<int:product_id>/', methods=['DELETE'])
def deleteProduct(product_id):
    for product in products_list:
        if product.ID == product_id:
            products_list.remove(product)
            return jsonify({'PRODUCTS': products_list}), 200
    abort(404)

# 404 errors handle
@products_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'ERROR': 'Not found'}), 404)

# 400 errors handle
@products_api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'ERROR': 'Bad Request'}), 400)