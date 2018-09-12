from flask import Flask, redirect, url_for, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources import (
    Store,
    StoreList,
    Item,
    ItemList,
    UserList,
    UserRegister,
    User,
    UserLogin,
    TokenRefresh
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# allow flask extensions to raise their own errors
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'my_key'
api = Api(app)
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback():
    return jsonify({
        'message': 'Request does not contain access token.',
        'error': 'no_token'
    }), 401


@jwt.needs_fresh_token_loader
def needs_fresh_callback():
    return jsonify({
        'message': 'Access token is not fresh.',
        'error': 'non_fresh_token'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'message': 'Access token has been revoked',
        'error': 'revoked_token'
    }), 401



@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    # TODO create index template
    redirect(url_for('index'))
    redirect(api.url_for(Item))
    return 'index template here'


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<string:name>')

api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/stores/<string:name>')

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
