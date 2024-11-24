from common.axios import Axios

def get_user_api():
    return Axios().get('/collections/usuario/records?filter=activo=true')

def get_users_api():
    return Axios().get('/collections/usuario/records?filter=activo=true')