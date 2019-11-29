from flask import Flask

from api.v1.addresses import addresses_api, Address
from api.v1.products import products_api, Product
from api.v1.orders import orders_api, Order
from api.v1.users import users_api, User

from flask.json import JSONEncoder

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Address):
            address = {
                'ID': obj.ID,
                'country': obj.country,
                'city': obj.city,
                'type_address': obj.type_address,
                'name': obj.name,
                'number': obj.number
            }
            if obj.floor is not None:
                address['floor'] = obj.floor
            if obj.stair is not None:
                address['stair'] = obj.stair
            return address
        if isinstance(obj, Order):
            return {
                'ID': obj.ID,
                'order_date': obj.order_date,
                'delivery_date': obj.delivery_date,
                'price': obj.price,
                'address': obj.address,
                'products': obj.products
            }
        if isinstance(obj, Product):
            return {
                'ID': obj.ID,
                'name': obj.name,
                'price': obj.price,
                'type_product': obj.type_product,
                'supplier': obj.supplier,
                'rate': obj.rate
            }
        if isinstance(obj, User):
            return {
                'ID': obj.ID,
                'password': '*********',
                'name': obj.name,
                'surnames': obj.surnames,
                'num_account': obj.num_account,
                'prime': obj.prime,
                'addresses': obj.addresses,
                'orders': obj.orders
            }
        return super(MyJSONEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = MyJSONEncoder

# Blueprint
app.register_blueprint(addresses_api)
app.register_blueprint(products_api)
app.register_blueprint(orders_api)
app.register_blueprint(users_api)

if __name__ == '__main__':
    app.run(debug=True)