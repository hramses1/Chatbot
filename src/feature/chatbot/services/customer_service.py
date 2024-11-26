from feature.chatbot.action.customer.get_customer_action import create_customer_action, get_customer_action
from feature.chatbot.action.appointment.get_appointment_action import create_appointment_with_detail
from feature.chatbot.models.customer_model import CustomerModel
from feature.chatbot.services.create_event_google_calendar_service import crear_evento_google_calendar
from feature.chatbot.utils.json_utils import get_all_data_from_json
from datetime import datetime

def crear_evento_para_cliente(user_info, service_details, fecha_actual):
    """Crea un evento en Google Calendar para un cliente."""
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

def crear_o_actualizar_cliente(user_info, service_details,observed):
    """Crea o actualiza un cliente y genera una cita."""
    try:
        # Crear cliente
        new_customer = CustomerModel(
            nombre=user_info["nombre"],
            identificacion=user_info["id"],
            correo=user_info["email"],
            correo_verificado=True,
            activo=True
        )
        created_customer = create_customer_action(new_customer)

        # Si el cliente ya existe
        if not created_customer:
            existing_customer = get_customer_action(user_info['email'])
            customer_id = existing_customer['items'][0]['id']
            print(f"Cliente existente: {user_info['nombre']} (ID: {customer_id})")
        else:
            customer_id = created_customer['id']
            print(f"Cliente creado exitosamente: {user_info['nombre']} (ID: {customer_id})")
            
            

        # Crear cita
        appointment_data = {
            "cliente": customer_id,
            "usuario": service_details["id_usuario"],
            "estado_caso": "En curso",
            "observacion": observed,
            "fecha_cita": datetime.now().isoformat()
        }
        detail_data = {
            "servicio": service_details['id_servicio'],
            "precio": service_details['precio_servicio']
        }

        create_appointment_with_detail(appointment_data, detail_data)
        print(f"Cita creada para el cliente: {user_info['nombre']}")
    except Exception as e:
        print(f"Error al procesar el cliente {user_info['nombre']}: {e}")

def process_form_submission():
    """Procesa la información del formulario para registrar clientes y citas."""
    try:
        # Extraer datos del formulario
        data = get_all_data_from_json()
        user_info = data.get("user_info")
        service_details = data.get("service_details")
        observed = f"Tienes un servicio {service_details['nombre_servicio']}, con el abogado {service_details['nombre_usuario']}: {service_details['correo_usuario']}"


        # Validar datos necesarios
        if not user_info or not service_details:
            print("Información incompleta en el formulario.")
            return

        print(f"Procesando usuario: {user_info['nombre']} ({user_info['email']})")

        # Procesar cliente y cita
        crear_o_actualizar_cliente(user_info, service_details,observed)

        # Crear evento en Google Calendar
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        crear_evento_para_cliente(user_info, service_details, fecha_actual)

    except Exception as e:
        print(f"Error al procesar la información del formulario: {e}")
