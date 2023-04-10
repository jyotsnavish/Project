from flask import Blueprint, jsonify, request
import requests
from models import db, Order, OrderItem

order_blueprint = Blueprint('order_api_routes',__name__,url_prefix='/api/order')

#get the current user by calling USER API
USER_API_URL = 'http://user-svc-c:5003/api/user'

def get_user(api_key):
    headers = {
        'Authorization': api_key
    }

    response = requests.get(USER_API_URL, headers=headers)
    print(response)
    if response.status_code != 200:
        return {'message' : 'Not Authorized'}
    
    user = response.json()
    return user


@order_blueprint.route('/',methods=['GET'])
def get_open_order():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message' : 'Not logged in'}), 401
    response = get_user(api_key)
    user = response.get('result')
    if not user:
        return jsonify({'message' : 'Not logged in'}), 401
    
    open_order = Order.query.filter_by(user_id=user['id'],is_open=1).first()
    if open_order:
        return jsonify({
            'result': open_order.serialize()
        }), 200
    else:
        return jsonify({'message': 'No open order'})

@order_blueprint.route('/all',methods=['GET'])
def get_all_orders():
    all_order = Order.query.all()
    result = [order.serialize() for order in all_order]
    return jsonify(result), 200

@order_blueprint.route('/add-item',methods=['POST'])
def create_order():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message' : 'Not logged in'}), 401
    response = get_user(api_key)
    print(response)
    if not response.get('result'):
        return jsonify({'message' : 'Not logged in'}), 401
    
    user = response.get('result')
    print(user)
    book_id = int(request.form['book_id'])
    quantity = int(request.form['quantity'])
    user_id = user['id']

    open_order = Order.query.filter_by(user_id=user_id,is_open=1).first()

    if not open_order:
        open_order = Order()
        open_order.is_open = True
        open_order.user_id = user_id

        order_item = OrderItem(book_id=book_id,quantity=quantity)
        open_order.order_items.append(order_item)

    else:
        found = False
        for item in open_order.order_items:
            if item.book_id == book_id:
                item.quantity += quantity
                found = True

        if not found:
            order_item  = OrderItem(book_id=book_id,quantity=quantity)
            open_order.order_items.append(order_item)

    db.session.add(open_order)
    db.session.commit()

    return jsonify({"result": open_order.serialize()})

@order_blueprint.route('/checkout',methods=['POST'])
def checkout_order():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message' : 'Not logged in'}), 401
    response = get_user(api_key)
    user = response.get('result')
    if not user:
        return jsonify({'message' : 'Not logged in'}), 401
    
    open_order = Order.query.filter_by(user_id=user['id'],is_open=1).first()

    if open_order:
        open_order.is_open=False

        db.session.add(open_order)
        db.session.commit()
        return jsonify({'result':open_order.serialize()})
    else:
        return jsonify({'message' : 'No open order'})