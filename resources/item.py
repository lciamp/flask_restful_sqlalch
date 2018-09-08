from flask_restful import Resource, reqparse
from flask import abort
from flask_jwt import jwt_required
import sqlite3
from decorators import db_check_or_return_500


class ItemList(Resource):
    def get(self):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query ="SELECT * FROM items"
            result = cursor.execute(query)
            rows = result.fetchall()
            items = [{'name': row[0], 'price': row[1]} for row in rows]
            connection.close()
        except:
            abort(500)
        return {'items': items}, 200


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Price field can not be left blank")

    @classmethod
    @db_check_or_return_500
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    @db_check_or_return_500
    def insert(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    @db_check_or_return_500
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    # @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)

        if item:
            return item, 200
        return {'message': "Item '{}' not found".format(name)}, 404

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()

        item = {
            "name": name,
            "price": data['price']
        }

        self.insert(item)

        return item, 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)

        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            self.insert(updated_item)
        else:
            self.update(updated_item)
        return updated_item, 200

    def delete(self, name):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()
        except:
            abort(500)

        return {'message': "Item '{}' deleted.".format(name)}, 202
