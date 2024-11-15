from feature.chatbot.action.customer.get_customer_action import create_customer_action
from feature.chatbot.models.customer_model import CustomerModel
from feature.chatbot.services.create_event_google_calendar_service import crear_evento_google_calendar
from feature.chatbot.utils.json_utils import get_all_data_from_json
from datetime import datetime

def crear_evento_para_cliente(user_info, service_details, fecha_actual):
    """Función para crear un evento en Google Calendar."""
    try:
        crear_evento_google_calendar(
            cliente_nombre=user_info['nombre'],
            cliente_email=user_info['email'],
            abogado_email=service_details['correo_usuario'],
            fecha=fecha_actual,
            hora_inicio=service_details['horario_usuario']['horario_inico'],
            duracion_minutos=service_details['horario_usuario']['tiempo_consulta']
        )
        print(f"Evento creado para el cliente: {user_info['nombre']}")
    except Exception as e:
        print(f"Error al crear evento para {user_info['nombre']}: {e}")

def process_form_submission():
    # Extraer todos los datos del archivo JSON
    data = get_all_data_from_json()

    # Verificar si la selección es válida


    # Obtener información del usuario y detalles del servicio
    user_info = data.get("user_info")
    service_details = data.get("service_details")
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    # Validar que la información del usuario y los detalles del servicio estén presentes
    if not user_info or not service_details:
        print("Información incompleta en el formulario.")
        return

    print(f"Procesando usuario: {user_info['nombre']} ({user_info['email']})")

    # Crear un nuevo cliente utilizando los datos extraídos
    new_customer = CustomerModel(
        nombre=user_info["nombre"],
        identificacion=user_info["id"],
        correo=user_info["email"],
        correo_verificado=True,
        activo=True
    )

    # Intentar crear el cliente
    try:
        created_customer = create_customer_action(new_customer)
        
        # Si el cliente se creó correctamente o ya existía, crear el evento
        if created_customer:
            print(f"Cliente creado exitosamente: {user_info['nombre']}")
        else:
            print(f"El cliente {user_info['nombre']} ya existe.")
        
        # Crear evento en Google Calendar
        crear_evento_para_cliente(user_info, service_details, fecha_actual)
    
    except Exception as e:
        print(f"Error al crear el cliente {user_info['nombre']}: {e}")
