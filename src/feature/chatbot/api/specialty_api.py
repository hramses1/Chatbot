from common.axios import Axios

def get_specialty_api():
    return Axios().get('/collections/especialidad/records?perPage=-1&sort=-created')

def get_specialties_api():
    return Axios().get('/collections/especialidad/records?perPage=-1&sort=-created')