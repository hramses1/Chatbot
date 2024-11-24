
from feature.chatbot.action.ws.ws_action import MessageActions

def send_message_service(to, message_type, **kwargs):
    """
    Servicio para enviar un mensaje usando UltraMsg.
    :param to: Número de teléfono del destinatario.
    :param message_type: Tipo de mensaje ('simple' o 'personalized').
    :param kwargs: Parámetros adicionales (como 'message', 'name', 'template').
    :return: Respuesta de la API UltraMsg.
    """
    actions = MessageActions()

    if message_type == "simple":
        if "message" not in kwargs:
            raise ValueError("El mensaje es requerido para mensajes simples.")
        return actions.send_simple_message(to, kwargs["message"])

    elif message_type == "personalized":
        if "name" not in kwargs or "template" not in kwargs:
            raise ValueError("El nombre y el template son requeridos para mensajes personalizados.")
        return actions.send_personalized_message(to, kwargs["name"], kwargs["template"])

    else:
        raise ValueError("Tipo de mensaje no soportado.")
