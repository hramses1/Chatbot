from common.axios import Axios
from config.config import URL_API_WS

class UltraMsgAPI:
    def __init__(self, instance_id, api_token):
        self.api_url = URL_API_WS
        self.api_token = api_token
        self.instance_id = instance_id

    def send_message(self, to, body):
        """Envía un mensaje a través de UltraMsg API."""
        payload = {
            "to": to,
            "body": body
        }
        headers = {
            "content-type": "application/json"
        }

        try:
            # Axios probablemente ya devuelve un dict, no necesita response.json()
            response = Axios(self.api_url).post(
                f"{self.instance_id}/messages/chat?token={self.api_token}",
                json=payload,
                headers=headers
            )
            # Si ya es un dict, simplemente retorna el resultado
            if isinstance(response, dict):
                return response
            # Si no es un dict, verifica el estado y convierte a JSON
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

