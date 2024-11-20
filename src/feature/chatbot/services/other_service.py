from feature.chatbot.action.specialty.get_specialties_action import get_specialties_action
import streamlit as st

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
        "🔍 **¿En qué área necesitas asesoría o quieres agendar una cita?**\n"
        "Selecciona la opción adecuada y organizaremos tu cita a la brevedad. 😊"
    )

def get_service_details_message(service, idx):
    """Despliega detalles del servicio seleccionado con diseño atractivo."""
    
    if f"expander_{idx}" not in st.session_state:
        st.session_state[f"expander_{idx}"] = False

    with st.expander(f"⭐ **Opción {idx+1}: {service.nombre_servicio}**", expanded=st.session_state[f"expander_{idx}"]):
        st.markdown(
            f"""
            <div style="padding: 10px; background-color: #f9f9f9; border-radius: 10px; border: 1px solid #ddd;">
                <p style="font-size: 16px; margin: 5px 0;"><strong>👨‍⚖️ Abogado:</strong> {service.nombre_usuario}</p>
                <p style="font-size: 16px; margin: 5px 0;"><strong>📄 Descripción:</strong> {service.descripcion_servicio}</p>
                <p style="font-size: 16px; margin: 5px 0;"><strong>💰 Precio:</strong> ${service.precio_servicio}</p>
                <p style="font-size: 15px; color: #555;">Si te interesa, <strong>¡contáctanos para agendar tu cita!</strong> 😊</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Cambiar estado del expander
        st.session_state[f"expander_{idx}"] = not st.session_state[f"expander_{idx}"]



def get_specialties_message():
    """Devuelve un mensaje con las especialidades disponibles como string."""
    specialties = get_specialties_action()

    if not specialties:
        return "No hay especialidades disponibles en este momento."

    # Crear un mensaje más visual usando un formato de lista
    specialties_message = "**🌟 Áreas de Especialidad:**\n"
    for index, specialty in enumerate(specialties, start=1):
        specialties_message += f"- **{index}. {specialty.name}**: {specialty.description}\n"
    
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
    "👏 **Excelente elección** 🎉. Has seleccionado al abogado **{nombre_usuario}** "
    "para el servicio **{nombre_servicio}**. 💼\n"
    "\n🎉 Opción seleccionada correctamente. ¿Te gustaría confirmar esta cita? (responde 'sí'✅ o 'no'❌)"
)