import requests

class BaseAxios:
    def __init__(self, base_url=None, headers=None):
        """
        Inicializa la clase BaseAxios con la URL base y las cabeceras predeterminadas.
        """
        self.base_url = base_url
        self.headers = headers or {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get(self, endpoint, params=None, headers=None):
        """
        Realiza una solicitud GET al endpoint especificado.
        """
        url = self._build_url(endpoint)
        try:
            response = requests.get(url, params=params, headers={**self.headers, **(headers or {})})
            return self._handle_response(response)
        except Exception as e:
            print(f"❌ Error en la solicitud GET: {e}")
            return None

    def post(self, endpoint, data=None, json=None, headers=None):
        """
        Realiza una solicitud POST al endpoint especificado.
        """
        url = self._build_url(endpoint)
        try:
            response = requests.post(url, data=data, json=json, headers={**self.headers, **(headers or {})})
            return self._handle_response(response)
        except Exception as e:
            print(f"❌ Error en la solicitud POST: {e}")
            return None

    def put(self, endpoint, data=None, json=None, headers=None):
        """
        Realiza una solicitud PUT al endpoint especificado.
        """
        url = self._build_url(endpoint)
        try:
            response = requests.put(url, data=data, json=json, headers={**self.headers, **(headers or {})})
            return self._handle_response(response)
        except Exception as e:
            print(f"❌ Error en la solicitud PUT: {e}")
            return None

    def delete(self, endpoint, headers=None):
        """
        Realiza una solicitud DELETE al endpoint especificado.
        """
        url = self._build_url(endpoint)
        try:
            response = requests.delete(url, headers={**self.headers, **(headers or {})})
            return self._handle_response(response)
        except Exception as e:
            print(f"❌ Error en la solicitud DELETE: {e}")
            return None

    def _build_url(self, endpoint):
        """
        Construye la URL completa utilizando la URL base y el endpoint proporcionado.
        """
        if self.base_url:
            return f"{self.base_url}{endpoint}"
        return endpoint

    def _handle_response(self, response):
        """
        Maneja la respuesta de la solicitud HTTP.
        """
        try:
            response.raise_for_status()  # Lanza un error para códigos 4xx y 5xx
            try:
                return response.json()  # Intenta devolver JSON si es posible
            except ValueError:
                print("⚠️ La respuesta no es un JSON válido.")
                return response.text  # Devuelve el texto si no es JSON
        except requests.exceptions.HTTPError as err:
            print(f"❌ Error HTTP ({response.status_code}): {err}")
            print(f"🔍 Detalle del error: {response.text}")
        except requests.exceptions.RequestException as err:
            print(f"❌ Error en la solicitud: {err}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        return response