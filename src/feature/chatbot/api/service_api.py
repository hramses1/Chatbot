from common.axios import Axios

def get_service_api():
    return Axios().get('/collections/servicio/records?perPage=-1&sort=-created')

def get_services_api():
    return Axios().get('/collections/servicio/records?perPage=-1&sort=-created')