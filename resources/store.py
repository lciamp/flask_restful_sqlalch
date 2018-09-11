from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}, 200


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': "Store '{}' not found".format(name)}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An store with name '{}' already exists".format(name)}, 400
        store = StoreModel(name)
        store.save_to_db()
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': "Store '{}' deleted.".format(name)}, 202
