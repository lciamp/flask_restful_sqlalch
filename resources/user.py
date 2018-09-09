import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.user import UserModel
from flask import abort


class User(Resource):

    @jwt_required()
    def get(self):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "SELECT * FROM users"
            result = cursor.execute(query)
            rows = result.fetchall()
            users = [{'name': row[1]} for row in rows]
            connection.close()
        except sqlite3.OperationalError:
            abort(500)
        return {'users': users}, 200


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username can not be blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password can not be blank"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created successfully.'}, 201







