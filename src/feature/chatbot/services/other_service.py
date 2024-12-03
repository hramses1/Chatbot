from config.config import USE_AI
from feature.chatbot.action.specialty.get_specialties_action import get_specialties_action
import streamlit as st

from feature.chatbot.api.groq_api import get_ai_response
from feature.chatbot.utils.bot_ultis import build_prompt_specialties

def get_welcome_message():
    """Devuelve el mensaje de bienvenida como string."""
    return (
        "👋 **¡Bienvenido/a al Estudio Jurídico!**\n"
        "🔹 Estamos aquí para ofrecerte soluciones legales personalizadas. "
        "Déjanos acompañarte en cada paso de tu proceso legal. "
        "Tu confianza es nuestra prioridad."
    )

def get_interest_query_message():
    """Devuelve el mensaje de consulta sobre el área de interés como string."""
    return (
        "✨ **Selecciona una opción para ayudarte mejor:**\n\n"
        "1️⃣ Agendar una cita\n\n"
        "2️⃣ Consultar tus citas\n\n"
        "Elige el número que prefieras y nos pondremos en contacto contigo enseguida. 😊"
    )


def get_service_details_message(service, idx):
    """Despliega detalles del servicio seleccionado."""
    if f"expander_{idx}" not in st.session_state:
        st.session_state[f"expander_{idx}"] = False

    with st.expander(f"⭐ **Opcion: {idx+1}** 👨‍⚖️ **Abogado**: {service.nombre_usuario}", expanded=st.session_state[f"expander_{idx}"]):
        st.markdown(f"**{service.nombre_servicio}**")
        st.markdown(f"📄 **Descripción**: {service.descripcion_servicio}")
        # st.markdown(f"💰 **Precio**: ${service.precio_servicio}")
        st.markdown(f"Horario de disponibilidad, **Desde: {service.horario_usuario["horario_inico"]} - Hasta: {service.horario_usuario["horario_fin"]}** 📅")
        st.markdown("Si te interesa, **¡contáctanos para agendar tu cita!** 😊")
        st.session_state[f"expander_{idx}"] = not st.session_state[f"expander_{idx}"]

def handle_schedule_appointment() -> str:
    """
    Maneja el flujo para agendar citas.

    Returns:
        str: Mensaje breve para guiar al usuario en el proceso de agendar una cita.
    """
    return (
        "🔍 **Cuéntanos tu caso** y organizaremos tu cita. 😊"
    )

def get_specialties_message():
    """Devuelve un mensaje con las especialidades disponibles como string."""
    specialties = get_specialties_action()

    if not specialties:
        return "No hay especialidades disponibles en este momento."

    # Crear un mensaje más visual usando un formato de lista
    specialties_message = "**🌟 Áreas de Especialidad:**\n"
    # print(specialties)
    
    prompt_specialties = build_prompt_specialties(specialties)

    if USE_AI == "True":
        print(prompt_specialties)
        get_ai_response(str(prompt_specialties))

    for index, specialty in enumerate(specialties, start=1):
        specialties_message += f"- 💼 **{specialty.name}**\n"
    
    return specialties_message
# Mensaje para seleccionar especialidades
SELECT_SPECIALTY_MESSAGE = (
    "🔍 Cuéntanos en qué podemos ayudarte. Selecciona una de nuestras especialidades a continuación:"
)

# Mensaje para consulta sobre servicios
ASK_FOR_SERVICE_MESSAGE = (
    "🔍 ¿En qué área necesitas asesoría? Elige el servicio que mejor se ajuste a tus necesidades."
)

# Mensaje de confirmación de cita
APPOINTMENT_CONFIRMED_MESSAGE = (
    "🎉 ¡Tu cita ha sido agendada exitosamente! Nos pondremos en contacto contigo pronto."
)

# Nuevo mensaje: Confirmación del servicio y abogado seleccionado
SERVICE_SELECTION_MESSAGE = (
    "👏 **Excelente elección** 🎉. Has seleccionado al abogado {nombre_usuario} "
    "para el servicio **{nombre_servicio}**. 💼\n"
    "\n🎉 Opción seleccionada correctamente. ¿Te gustaría confirmar esta cita? (responde 'si'✅ o 'no'❌)"
)

def create_custom_message(data, estimated_time):
    """
    Genera un mensaje personalizado para el usuario.
    
    :param data: Diccionario con la información del usuario (incluye 'nombre').
    :param estimated_time: Diccionario con los detalles de la cita (incluye 'start_time').
    :return: Cadena con el mensaje personalizado.
    """
    return (
        f"Estimado/a {data['nombre']},\n\n"
        f"Le recordamos que tiene una cita programada para el día {estimated_time['start_time']}.\n"
        f"📧 Por favor, revise su correo electrónico para aceptar la invitación a la reunión. "
        f"En caso de no encontrarla en su bandeja de entrada, le sugerimos revisar también su carpeta de spam o correo no deseado.\n\n"
        f"Gracias por su atención.\n\n"
        f"Saludos cordiales."
    )