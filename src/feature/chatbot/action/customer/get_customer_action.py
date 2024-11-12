from typing import List, Optional, Dict
from feature.chatbot.api.customer_api import get_customers_api, create_customer_api
from feature.chatbot.models.customer_model import CustomerModel


def get_customer_action(identificacion: str) -> Optional[List[CustomerModel]]:
    """
    Obtiene información del cliente basado en la identificación proporcionada.

    Args:
        identificacion (str): Identificación del cliente.

    Returns:
        Optional[List[CustomerModel]]: Lista de clientes que coinciden con la identificación proporcionada, o None si no hay coincidencias.
    """
    try:
        response = get_customers_api()
        if not response or "items" not in response:
            return None

        # Filtrar los clientes que coinciden con la identificación proporcionada
        customers = [
            CustomerModel(
                id=item.get("id"),
                nombre=item.get("nombre"),
                identificacion=item.get("identificacion"),
                correo=item.get("correo"),
                correo_verificado=item.get("correo_verificado"),
                activo=item.get("activo"),
                genero=item.get("genero"),
                define_horario=item.get("define_horario"),
                horario=item.get("horario"),
                usuario_crea_id=item.get("usuario_crea_id"),
                usuario_actualiza_id=item.get("usuario_actualiza_id"),
                borrado=item.get("borrado")
            )
            for item in response["items"] if item.get("identificacion") == identificacion
        ]

        return customers if customers else None

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
        if response and response.get("success"):
            return CustomerModel(
                id=response.get("id"),
                nombre=response.get("nombre"),
                identificacion=response.get("identificacion"),
                correo=response.get("correo"),
                correo_verificado=response.get("correo_verificado"),
                activo=response.get("activo"),
                usuario_crea_id=response.get("usuario_crea_id"),
                usuario_actualiza_id=response.get("usuario_actualiza_id"),
                borrado=response.get("borrado")
            )
        else:
            print("Error al crear el cliente.")
            return None

    except Exception as e:
        print(f"Error al crear el cliente: {e}")
        return None
