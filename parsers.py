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

