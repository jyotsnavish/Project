import requests
from flask import session
from . import ORDER_API_URL

class OrderClient:
    @staticmethod
    def get_order():
        headers = {
            'Authorization' : session['user_api_key']
        }
        url = ORDER_API_URL + '/api/order'
        response = requests.get(url,headers=headers)
        return response.json()
    
    @staticmethod
    def add_to_cart(book_id,quantity=1):
        payload={
            'book_id':book_id,
            'quantity':quantity
        }
        header={
            'Authorization' : session['user_api_key']
        }
        url = ORDER_API_URL + '/api/order/add-item'
        response = requests.post(url,data=payload,headers=header)
        return response.json()
    
    @staticmethod
    def checkout():
        header={
            'Authorization' : session['user_api_key']
        }
        url = ORDER_API_URL + '/api/order/checkout'
        response = requests.post(url,headers=header)
        return response.json()
    
    @staticmethod
    def get_order_session():
        default_order={
            'items': {}
        }
        return session.get('order',default_order)