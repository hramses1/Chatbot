from typing import List, Optional, Dict
from feature.chatbot.api.user_api import get_users_api


def get_user_action(id: str) -> Optional[List[Dict[str, str]]]:
    try:
        response = get_users_api()
        users = []

        # Buscar todos los registros que coinciden con los usuarios
        for item in response["items"]:
            if item["id"] == id:
                users.append({
                    "name": item["nombre"],
                    "username": item["username"],
                    "email": item["email"],
                    "status": item["activo"],
                    "gender": item["genero"],
                    "define_schedule": item["define_horario"],
                    "schedule": item["horario"]
                })

        # Retorna la lista de usuario encontrados o None si está vacía
        return users if users else None

    except Exception as e:
        print(e)
        return None