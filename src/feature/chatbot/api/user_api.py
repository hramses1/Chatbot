from common.axios import Axios

def get_user_api():
    return Axios().get('/collections/usuario/records?perPage=-1&sort=-created')

def get_users_api():
    return Axios().get('/collections/usuario/records?perPage=-1&sort=-created')