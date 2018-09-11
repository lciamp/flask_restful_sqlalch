from flask_restful import reqparse


item_parser = reqparse.RequestParser()
item_parser.add_argument('price',
                         type=float,
                         required=True,
                         location='json',
                         help="price field can not be left blank")
item_parser.add_argument('store_id',
                         type=int,
                         location='json',
                         required=True,
                         help="store_id field can not be left blank")


user_parser = reqparse.RequestParser()
user_parser.add_argument('username',
                         type=str,
                         required=True,
                         location='json',
                         help="Username can not be blank"
                         )
user_parser.add_argument('password',
                         type=str,
                         required=True,
                         location='json',
                         help="Password can not be blank"
                         )
