from common.axios import Axios

def get_categories_api():
    return Axios().get('/collections/categoria/records?filter=activo=true')

def get_category_api():
    return Axios().get('/collections/categoria/records?filter=activo=true')