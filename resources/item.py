from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from models.item import ItemModel

_item_parser = reqparse.RequestParser()
_item_parser.add_argument('price',
                          type=float,
                          required=True,
                          location='json',
                          help="price field can not be left blank"
                          )
_item_parser.add_argument('store_id',
                          type=int,
                          location='json',
                          required=True,
                          help="store_id field can not be left blank"
                          )


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.find_all()]}, 200


class Item(Resource):
    @jwt_required
    def get(self, name):
        print(current_user.username)
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(), 200

        return {'message': "Item '{}' not found".format(name)}, 404

    @jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = _item_parser.parse_args()

        item = ItemModel(name,  **data)

        item.save_to_db()

        return item.json(), 201

    @jwt_required
    def put(self, name):
        data = _item_parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json(), 202

    @jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': "Item '{}' deleted.".format(name)}, 202
