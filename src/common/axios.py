from common.base_axios import BaseAxios
from config.config import URL_API

class Axios(BaseAxios):
    def __init__(self, base_url=None, headers=None):
        """
        Inicializa la clase Axios con la URL base y cabeceras personalizadas.
        """
        # Configura la URL base y las cabeceras, fusionando con las predeterminadas
        base_url = base_url or URL_API
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            **(headers or {})
        }
        
        # Llama al constructor de la clase base con los valores ajustados
        super().__init__(base_url=base_url, headers=headers)
