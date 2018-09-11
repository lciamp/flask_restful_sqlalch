from flask_restful import Resource
from flask_jwt import jwt_required
from models.user import UserModel
from parsers import user_parser


class UserList(Resource):

    @jwt_required()
    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}, 200


class UserRegister(Resource):
    def post(self):
        data = user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': "User '{}' created successfully.".format(user.username)}, 201







