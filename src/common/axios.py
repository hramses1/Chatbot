from common.base_axios import BaseAxios
from config.config import URL_API

class Axios(BaseAxios):
    def __init__(self, base_url=None, headers=None):
        self.base_url = base_url
        self.headers = headers or {}

        super().__init__(
            base_url=URL_API
        )

    
