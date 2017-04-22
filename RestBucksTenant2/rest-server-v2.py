#!flask/bin/python

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

from flask import Flask, request, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()
#client = MongoClient('localhost', 27017)
client = MongoClient('ec2-52-53-152-19.us-west-1.compute.amazonaws.com', 27017)
db = client['restbucks']
orders = db['orders'] 

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)
'''
orders = [
    {
        'location': 1,
        'status': u'Buy groceries',
        'message': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'items':[{
            'size':u'small',
            'milk':u'mocha',
            'name':u'name',
            'qty':1
        }]
    },
    {
        'location': 2,
        'status': u'Buy groceries',
        'message': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'items':[{
            'size':u'large',
            'milk':u'mocha',
            'name':u'name',
            'qty':21
        }]
    }
]
'''
order_fields = {
    '_id': fields.String,
    'location': fields.String,
    'status': fields.String,
    'message': fields.String,
    'items': fields.Nested({
        'size': fields.String,
        'milk': fields.String,
        'name': fields.String,
        'qty': fields.Integer
    })    
    #'uri': fields.Url('task')
}

class OrderListAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('location', type=str, location=['json', 'form'])
        self.reqparse.add_argument('status', type=str, location=['json', 'form'])
        self.reqparse.add_argument('message', type=str, location=['json', 'form'])
        self.reqparse.add_argument('items', type=list, location='json')
        self.reqparse.add_argument('size', type=str, location=['json', 'form'])
        self.reqparse.add_argument('name', type=str, location=['json', 'form'])
        self.reqparse.add_argument('milk', type=str, location=['json', 'form'])
        self.reqparse.add_argument('qty', type=int, location=['json', 'form'])
        super(OrderListAPI, self).__init__()

    def get(self):
        allOrders = orders.find()
        return {'orders': [marshal(order, order_fields) for order in allOrders]}

    def post(self):
        args=request.get_json(force=True)
        order = {
            'location': args['location'],
            'status': 'PLACED',
            'items': args['items'],
            'message': 'Your order has been placed'
        }
        #orders.append(order)
        order_id = orders.insert_one(order).inserted_id
        order_saved=orders.find_one({"_id":order_id})
        print order_id
        order_json = marshal(order_saved, order_fields)
        #order_json['_id']= (str)order_id
        print order_json
        return {'order': order_json }, 201

class PayOrderAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('location', type=str, location='json')
        self.reqparse.add_argument('status', type=str, location='json')
        self.reqparse.add_argument('message', type=str, location='json')
        self.reqparse.add_argument('items', type=[], location='json')
        self.reqparse.add_argument('size', type=str, location='json')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('milk', type=str, location='json')
        self.reqparse.add_argument('qty', type=int, location='json')
        super(PayOrderAPI, self).__init__()

    def post(self,id,pay):
        if pay!="pay":
            abort(404)
        order = orders.find_one({"_id": ObjectId(id)})
        if order is None:
            abort(404)
        
        if len(order) == 0:
            abort(404)
        
        if order['status']!="PLACED":
            abort(412)
       
        #args = self.reqparse.parse_args()
        args=request.get_json(force=True)
        order['message']= 'PAYMENT ACCEPTED'
        order['status']= 'PAID'
        print "Paid"
        orders.save(order)
        return {'order': marshal(order, order_fields)},201

class OrderAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('location', type=str, location='json')
        self.reqparse.add_argument('status', type=str, location='json')
        self.reqparse.add_argument('message', type=str, location='json')
        self.reqparse.add_argument('items', type=[], location='json')
        self.reqparse.add_argument('size', type=str, location='json')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('milk', type=str, location='json')
        self.reqparse.add_argument('qty', type=int, location='json')
        super(OrderAPI, self).__init__()

    def get(self, id):
        #order = [order for order in orders if order['location'] == id]
        order = orders.find_one({"_id": ObjectId(id)})
        print order
        if order is None:
            abort(404)
        if len(order) == 0:
            abort(404)
        return {'order': marshal(order, order_fields)}

    def put(self, id):
        #order = [order for order in orders if order['location'] == id]
        order = orders.find_one({"_id": ObjectId(id)})
        if order is None:
            abort(404)
        if len(order) == 0:
            abort(404)
        #args = self.reqparse.parse_args()
        args=request.get_json(force=True)
        for k, v in args.items():
            if v is not None:
                order[k] = v
        orders.save(order)
        return {'order': marshal(order, order_fields)}

    def delete(self, id):
        order = orders.find_one({"_id": ObjectId(id)})
        if order is None:
            abort(404)
        if len(order) == 0:
            abort(404)
        orders.remove({"_id": ObjectId(id)})
        return {'result': True}


api.add_resource(OrderListAPI, '/orders', endpoint='orders')
api.add_resource(OrderAPI, '/orders/<string:id>', endpoint='order')
api.add_resource(PayOrderAPI, '/order/<string:id>/<string:pay>', endpoint='pay')

if __name__ == '__main__':
    app.run(debug=True)
