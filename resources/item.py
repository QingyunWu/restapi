from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    # only pass the price argument
    parser.add_argument('price', type=float, required=True, help="needs price")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id")



    @jwt_required() # authenticate before call get method, here we need the JWT to call get method
    def get(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            return item.json()
        return {'msg': 'item not found'}, 404

    def post(self, name):
        if ItemModel.get_item_by_name(name):
            return {'msg': "AN item with name '{}' already exists".format(name)}, 400 #bad request
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        print item.name
        print item.price
        try:
            item.save_to_db()
        except:
            return {'msg': 'An error occurred inserting the item'}, 500#internal server error
        return item.json(), 201 # 201 created, 202 accepted



    def delete(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            item.delete_from_db()
            return {'msg': 'item delted'}
        return {'msg': 'item not found'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.get_item_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json() # show to the browser




class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
