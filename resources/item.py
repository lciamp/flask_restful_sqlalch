from flask_restful import Resource, reqparse
from flask import abort
from flask_jwt import jwt_required, current_identity
import sqlite3
from models.item import ItemModel


class ItemList(Resource):
    def get(self):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "SELECT * FROM items ORDER BY name"
            result = cursor.execute(query)
            rows = result.fetchall()
            items = [{'name': row[0], 'price': row[1]} for row in rows]
            connection.close()
        except sqlite3.OperationalError:
            abort(500)
        return {'items': items}, 200


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Price field can not be left blank")

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

        item = ItemModel(name,  data['price'])

        item.insert()

        return item.json(), 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        updated_item = ItemModel(name, data['price'])
        if item is None:
            updated_item.insert()
        else:
            updated_item.update()
        return updated_item.json(), 200

    @jwt_required()
    def delete(self, name):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()
        except sqlite3.OperationalError:
            abort(500)

        return {'message': "Item '{}' deleted.".format(name)}, 202
