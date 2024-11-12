from common.axios import Axios

def get_customer_api():
    return Axios().get('/collections/cliente/records?perPage=-1&sort=-created')

def get_customers_api():
    return Axios().get('/collections/cliente/records?perPage=-1&sort=-created')

def create_customer_api(data = None, json = None):
    return Axios().post('/collections/cliente/records?perPage=-1&sort=-created', data=data, json=json)