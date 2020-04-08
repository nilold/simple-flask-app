from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "LM12AS5h7suM8UW6ds2l8Hn34s5"
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="price cannot be blank!"
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda i: i["name"] == name, items), None)

        if item:
            return item, 200
        return None, 404

    # @jwt_required()
    def post(self, name):
        data = Item.parser.parse_args()

        if next(filter(lambda i: i["name"] == name, items), None) is not None:
            return {"message": f"An item with name {name} already exists"}, 400

        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    # @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda i: i["name"] != name, items))
        return {"message": f"{name} deleted"}

    # @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda i: i["name"] == name, items), None)
        if not item:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)

        return item


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {"items": items}, 200


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
