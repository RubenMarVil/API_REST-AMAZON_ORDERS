# -*- coding: utf-8 -*

from api.v1.addresses import addresses_list, Address
from api.v1.orders import orders_list, Order

from flask import Blueprint, jsonify, abort, make_response, request

class User:
    def __init__(self, ID, password, name, surnames, num_account, prime, addresses, orders):
        self.ID = ID
        self.password = password
        self.name = name
        self.surnames = surnames
        self.num_account = num_account
        self.prime = prime
        self.addresses = addresses
        self.orders = orders

##############################################################################
# DATA
users_list = [User('83792074D', 'albertito', 'Alberto', 'Gonzalez', '7693-8123-7854-8572', True, [addresses_list[2], addresses_list[0]], [orders_list[0]]),
User('75493182G', 'tractores28', 'Maria', 'Jimenez', '7526-8547-5857-5825', False, [addresses_list[1]], [orders_list[1]])]
##############################################################################

users_api = Blueprint('users_api', __name__)

# Get all users
@users_api.route('/v1/users/', methods=['GET'])
def getUsers():
    return jsonify({'USERS': users_list}), 200

# Get one users from his/her ID(DNI)
@users_api.route('/v1/users/<string:user_id>/', methods=['GET'])
def getOneUser(user_id):
    for user in users_list:
        if user.ID == user_id:
            return jsonify({'USER': user}), 200
    abort(404)

# Create one user
@users_api.route('/v1/users/', methods=['POST'])
def createUser():
    if not request.json or not 'ID' in request.json:
        abort(400)
    ID = request.json.get('ID')
    password = request.json.get('password')
    name = request.json.get('name')
    surnames = request.json.get('surnames')
    num_account = request.json.get('surnames')
    prime = request.json.get('prime')
    new_user = User(ID, password, name, surnames, num_account, prime, [], [])
    users_list.append(new_user)
    return jsonify({'USER-CREATED': new_user}), 201

# Edit one user
@users_api.route('/v1/users/<string:user_id>/', methods=['PUT'])
def editUser(user_id):
    if request.json:
        for user in users_list:
            if user.ID == user_id:
                if 'password' in request.json:
                    user.password = request.json.get('password')
                if 'name' in request.json:
                    user.name = request.json.get('name')
                if 'surnames' in request.json:
                    user.surnames = request.json.get('surnames')
                if 'num_account' in request.json:
                    user.num_account = request.json.get('num_account')
                if 'prime' in request.json:
                    user.prime = request.json.get('prime')
                return jsonify({'USER-EDITED': user}), 201
        abort(404)
    abort(400)

# Delete one user
@users_api.route('/v1/users/<string:user_id>/', methods=['DELETE'])
def deleteUser(user_id):
    for user in users_list:
        if user.ID == user_id:
            users_list.remove(user)
            return jsonify({'USERS': users_list}), 200
    abort(404)

# Get all addresses of one user
@users_api.route('/v1/users/<string:user_id>/addresses/', methods=['GET'])
def getAddressesOfUser(user_id):
    for user in users_list:
        if user.ID == user_id:
            return jsonify({'ADDRESSES': user.addresses}), 200
    abort(404)

# Get one address of one user
@users_api.route('/v1/users/<string:user_id>/addresses/<int:address_id>/', methods=['GET'])
def getOneAddressOfUser(user_id, address_id):
    for user in users_list:
        if user.ID == user_id:
            for address in user.addresses:
                if address.ID == address_id:
                    return jsonify({'ADDRESS': address}), 200
    abort(404)

# Create one address to one user
@users_api.route('/v1/users/<string:user_id>/addresses/', methods=['POST'])
def createAddressToUser(user_id):
    if not request.json or not 'country' in request.json:
        abort(400)
    for user in users_list:
        if user.ID == user_id:
            ID = addresses_list[-1].ID + 1
            country = request.json.get('country')
            city = request.json.get('city')
            type_address = request.json.get('type_address')
            name = request.json.get('name')
            number = request.json.get('number')
            if 'stair' in request.json:
                stair = request.json.get('stair')
            else:
                stair = None
            if 'floor' in request.json:
                floor = request.json.get('floor')
            else:
                floor = None
            new_address = Address(ID, country, city, type_address, name, number, stair, floor)
            addresses_list.append(new_address)
            user.addresses.append(new_address)
            return jsonify({'ADDRESS-CREATED': user.addresses}), 201
    abort(404)

# Delete one address to one user
@users_api.route('/v1/users/<string:user_id>/addresses/<int:address_id>/', methods=['DELETE'])
def deleteAddressOfUser(user_id, address_id):
    for user in users_list:
        if user.ID == user_id:
            for address in addresses_list:
                if address in user.addresses:
                    user.addresses.remove(address)
                    return jsonify({'ADDRESSES': user.addresses}), 200
    abort(404)

# Get all orders of one user
@users_api.route('/v1/users/<string:user_id>/orders/', methods=['GET'])
def getOrdersOfUser(user_id):
    for user in users_list:
        if user.ID == user_id:
            return jsonify({'ORDERS': user.orders}), 200
    abort(404)

# Get one order of one user
@users_api.route('/v1/users/<string:user_id>/orders/<int:order_id>/', methods=['GET'])
def getOneOrderOfUser(user_id, order_id):
    for user in users_list:
        if user.ID == user_id:
            for order in user.orders:
                if order.ID == order_id:
                    return jsonify({'ORDER': order}), 200
    abort(404)

# Create one order to one user
@users_api.route('/v1/users/<string:user_id>/orders/', methods=['POST'])
def createOrderToUser(user_id):
    if not request.json or not 'order_date' in request.json:
        abort(400)
    for user in users_list:
        if user.ID == user_id:
            ID = orders_list[-1].ID + 1
            order_date = request.json.get('order_date')
            delivery_date = request.json.get('delivery_date')
            new_order = Order(ID, order_date, delivery_date, 0.00, None, [])
            orders_list.append(new_order)
            user.orders.append(new_order)
            return jsonify({'ORDER-CREATED': new_order}), 201
    abort(404)

# 404 errors handle
@users_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'ERROR': 'Not found'}),404)

# 400 errors handle
@users_api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'ERROR': 'Bad Request'}),400)

# 401 errors handle
@users_api.errorhandler(401)
def unauthorised(error):
    return make_response(jsonify({'ERROR': 'Unauthorised'}),401)