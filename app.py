from flask import Flask, redirect, url_for
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
    UserLogin
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


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
