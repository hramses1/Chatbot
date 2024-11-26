from typing import List, Optional
from feature.chatbot.models.customer_state_cases_model import ClienteCasoCorreoResponse
from feature.chatbot.models.service_user_view_model import ServiceUserViewModel
from feature.chatbot.api.service_user_view_api import (
    get_customer_state_cases_api,
    get_service_user_for_user_api,
    get_service_user_for_id_specialty_api
)

def get_service_user_by_name(user: str) -> Optional[List[ServiceUserViewModel]]:
    """
    Obtiene los servicios asignados a un abogado basado en su nombre de usuario.

    Args:
        user (str): Nombre del usuario (abogado).

    Returns:
        Optional[List[ServiceUserViewModel]]: Lista de servicios asociados al usuario, o None si no se encuentran.
    """
    try:
        response = get_service_user_for_user_api(user)
        if not response or "items" not in response:
            return None

        services = [
            ServiceUserViewModel(
                collectionId=item.get("collectionId"),
                collectionName=item.get("collectionName"),
                correo_usuario=item.get("correo_usuario"),
                descripcion_servicio=item.get("descripcion_servicio"),
                genero_usuario=item.get("genero_usuario"),
                horario_usuario=item.get("horario_usuario"),
                horario_inico=item.get("horario_inico"),
                horario_fin=item.get("horario_fin"),
                tiempo_consulta=item.get("tiempo_consulta"),
                id=item.get("id"),
                id_especialidad=item.get("id_especialidad"),
                id_servicio=item.get("id_servicio"),
                id_usuario=item.get("id_usuario"),
                nombre_servicio=item.get("nombre_servicio"),
                nombre_usuario=item.get("nombre_usuario"),
                precio_servicio=item.get("precio_servicio")
            )
            for item in response["items"]
        ]

        return services if services else None

    except Exception as e:
        print(f"Error al obtener los servicios para el usuario {user}: {e}")
        return None

def get_service_user_by_specialty(id_specialty: str) -> Optional[List[ServiceUserViewModel]]:
    """
    Obtiene los servicios basados en el ID de especialidad.

    Args:
        id_specialty (str): ID de la especialidad.

    Returns:
        Optional[List[ServiceUserViewModel]]: Lista de servicios asociados a la especialidad, o None si no se encuentran.
    """
    try:
        response = get_service_user_for_id_specialty_api(id_specialty)
        if not response or "items" not in response:
            return None

        services = [
            ServiceUserViewModel(
                collectionId=item.get("collectionId"),
                collectionName=item.get("collectionName"),
                correo_usuario=item.get("correo_usuario"),
                descripcion_servicio=item.get("descripcion_servicio"),
                genero_usuario=item.get("genero_usuario"),
                horario_usuario=item.get("horario_usuario"),
                horario_inico=item.get("horario_inico"),
                horario_fin=item.get("horario_fin"),
                tiempo_consulta=item.get("tiempo_consulta"),
                id=item.get("id"),
                id_especialidad=item.get("id_especialidad"),
                id_servicio=item.get("id_servicio"),
                id_usuario=item.get("id_usuario"),
                nombre_servicio=item.get("nombre_servicio"),
                nombre_usuario=item.get("nombre_usuario"),
                precio_servicio=item.get("precio_servicio")
            )
            for item in response["items"]
        ]

        return services if services else None

    except Exception as e:
        print(f"Error al obtener los servicios para la especialidad {id_specialty}: {e}")
        return None
from typing import Optional
from pydantic import ValidationError

def get_customer_state_cases(email: str) -> Optional[ClienteCasoCorreoResponse]:
    """
    Función para obtener los casos de estado de un cliente basado en su correo electrónico.
    """
    try:
        # Realiza la llamada a la API pasando el parámetro email
        response = get_customer_state_cases_api(email)

        # Accede al contenido JSON de la respuesta
        api_response = response  # Convertimos el Response en un diccionario

        # Valida y convierte la respuesta al modelo
        customer_cases = ClienteCasoCorreoResponse(**api_response)
        return customer_cases
    except ValidationError as e:
        # Manejo de errores de validación del modelo
        print(f"Error de validación de datos: {e}")
        return None
    except RuntimeError as e:
        # Manejo de errores de conexión con la API
        print(f"Error al obtener los casos del cliente: {e}")
        return None

