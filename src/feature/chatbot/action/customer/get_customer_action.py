from typing import  Optional
from feature.chatbot.api.customer_api import get_customer_api, create_customer_api
from feature.chatbot.models.customer_model import CustomerModel
from feature.chatbot.utils.json_utils import save_to_json


def get_customer_action(correo: str):
    """
    Obtiene información del cliente basado en la identificación proporcionada.

    Args:
        identificacion (str): Identificación del cliente.

    Returns:
        Optional[List[CustomerModel]]: Lista de clientes que coinciden con la identificación proporcionada, o None si no hay coincidencias.
    """
    try:
        response = get_customer_api(correo)
        return response['items'] if response else None

    except Exception as e:
        print(f"Error al obtener el cliente: {e}")
        return None


def create_customer_action(data: CustomerModel) -> Optional[CustomerModel]:
    """
    Crea un nuevo cliente utilizando la API.

    Args:
        data (CustomerModel): Datos del cliente a crear.

    Returns:
        Optional[CustomerModel]: Cliente creado o None si falla.
    """
    try:
        # Validar que los campos obligatorios estén presentes
        if not data.nombre or not data.identificacion or not data.correo:
            print("Error: Los campos 'nombre', 'identificacion' y 'correo' son obligatorios.")
            return None

        # Convertir el modelo en un diccionario para enviarlo a la API
        payload = data.dict()

        # Llamar a la API para crear el cliente
        response = create_customer_api(payload)

        # Validar la respuesta de la API
        if response :
            save_to_json({"status_appointment": True})
            return response
        else:
            print("Error al crear el cliente.")
            save_to_json({"status_appointment": False})
            return None

    except Exception as e:
        print(f"Error al crear el cliente: {e}")
        return None
