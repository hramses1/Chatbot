from common.axios import Axios

def get_categories_api():
    return Axios().get('/collections/categoria/records?perPage=-1&sort=-created')

def get_category_api():
    return Axios().get('/collections/categoria/records?perPage=-1&sort=-created')