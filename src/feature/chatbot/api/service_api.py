from common.axios import Axios

def get_service_api():
    return Axios().get('/collections/servicio/records?filter=activo=true')

def get_services_api():
    return Axios().get('/collections/servicio/records?filter=activo=true')