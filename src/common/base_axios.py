import requests

class BaseAxios:
    def __init__(self, base_url=None, headers=None):
        self.base_url = base_url
        self.headers = headers or {}

    def get(self, endpoint, params=None, headers=None):
        url = self._build_url(endpoint)
        response = requests.get(url, params=params, headers={**self.headers, **(headers or {})})
        return self._handle_response(response)

    def post(self, endpoint, data=None, json=None, headers=None):
        url = self._build_url(endpoint)
        response = requests.post(url, data=data, json=json, headers={**self.headers, **(headers or {})})
        return self._handle_response(response)

    def put(self, endpoint, data=None, json=None, headers=None):
        url = self._build_url(endpoint)
        response = requests.put(url, data=data, json=json, headers={**self.headers, **(headers or {})})
        return self._handle_response(response)

    def delete(self, endpoint, headers=None):
        url = self._build_url(endpoint)
        response = requests.delete(url, headers={**self.headers, **(headers or {})})
        return self._handle_response(response)

    def _build_url(self, endpoint):
        if self.base_url:
            return f"{self.base_url}{endpoint}"
        return endpoint

    def _handle_response(self, response):
        try:
            response.raise_for_status()  # Lanza un error para códigos 4xx y 5xx
            return response.json()  # Retorna JSON si es posible
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return None
        except ValueError:
            # Si la respuesta no es JSON, retorna el texto
            return response.text
        except Exception as err:
            print(f"An error occurred: {err}")
            return None
