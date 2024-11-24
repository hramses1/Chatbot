from common.axios import Axios

def get_specialty_api():
    return Axios().get('/collections/especialidad/records?filter=activo=true')

def get_specialties_api():
    return Axios().get('/collections/especialidad/records?filter=activo=true')