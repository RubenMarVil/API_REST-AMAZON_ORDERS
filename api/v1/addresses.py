# -*- coding: utf-8 -*

from flask import Blueprint, jsonify, abort, make_response, request

class Address:
    def __init__(self, ID, country, city, type_address, name, number, stair, floor):
        self.ID = ID
        self.country = country
        self.city = city
        self.type_address = type_address
        self.name = name
        self.number = number
        self.stair = stair
        self.floor = floor

##############################################################################
# DATA
addresses_list = [Address(1, 'Spain', 'Madrid', 'Street', 'Pablo Picasso', 8, 2, 4),
Address(2, 'United Kingdom', 'London', 'Avenue', '23', 4, None, None),
Address(3, 'Spain', 'Ciudad Real', 'Street', 'San Anton', 6, 0, 0)]
##############################################################################

addresses_api = Blueprint('addresses_api', __name__)

# Get all addresses
@addresses_api.route('/v1/addresses/', methods=['GET'])
def getAddresses():
    return jsonify({'ADDRESSES': addresses_list}), 200

# Get one address from his ID
@addresses_api.route('/v1/addresses/<int:address_id>/', methods=['GET'])
def getOneAddress(address_id):
    for address in addresses_list:
        if address.ID == address_id:
            return jsonify({'ADDRESS': address}), 200
    abort(404)

# Create one address
@addresses_api.route('/v1/addresses/', methods=['POST'])
def createAddress():
    if not request.json or not 'country' in request.json:
        abort(400)
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
    return jsonify({'ADDRESS-CREATED': new_address}), 201

# Edit one address
@addresses_api.route('/v1/addresses/<int:address_id>/', methods=['PUT'])
def editAddress(address_id):
    if request.json:
        for address in addresses_list:
            if address.ID == address_id:
                if 'country' in request.json:
                    address.country = request.json.get('country')
                if 'city' in request.json:
                    address.city = request.json.get('city')
                if 'type_address' in request.json:
                    address.type_address = request.json.get('type_address')
                if 'name' in request.json:
                    address.name = request.json.get('name')
                if 'number' in request.json:
                    address.number = request.json.get('number')
                if 'stair' in request.json:
                    address.stair = request.json.get('stair')
                if 'floor' in request.json:
                    address.floor = request.json.get('floor')
                return jsonify({'ADDRESS-EDITED': address}), 201
        abort(404)
    abort(400)

# Delete one address
@addresses_api.route('/v1/addresses/<int:address_id>/', methods=['DELETE'])
def deleteAddress(address_id):
    for address in addresses_list:
        if address.ID == address_id:
            addresses_list.remove(address)
            return jsonify({'ADDRESSES': addresses_list}), 200
    abort(404)

# 404 errors handle
@addresses_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'ERROR': 'Not found'}), 404)

# 400 errors handle
@addresses_api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'ERROR': 'Bad Request'}),400)