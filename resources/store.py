from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return store.json(), 200
        return {'msg': 'store not found'}, 404

    def post(self, name):
        if StoreModel.get_store_by_name(name):
            return {'msg': 'store {} already exists'.format(name)}, 400 #bad Request
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'msg': 'error occurred'}, 500 # internal server error

        return store.json(), 201 # created


    def delete(self, name):
        store = StoreModel.get_store_by_name(name)
        if store:
            store.delete_from_db()
            return {'msg': 'store deleted'}
        else:
            return {'msg': 'no such store: {}'.format(name)}

class StoreList(Resource):
    def get(self):
        return {'store': [store.json() for store in StoreModel.query.all()]}
