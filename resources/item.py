from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        location='json',
                        help="price field can not be left blank")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        location='json',
                        help="store_id field can not be left blank")

    def get(self, name):
        # user = current_identity
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(), 200
        return {'message': "Item '{}' not found".format(name)}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name,  **data)

        item.save_to_db()

        return item.json(), 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json(), 202

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': "Item '{}' deleted.".format(name)}, 202
