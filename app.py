from flask import Flask, redirect, url_for
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'my_key'
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth


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
api.add_resource(Item, '/item/<string:name>')
api.add_resource(User, '/users')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)