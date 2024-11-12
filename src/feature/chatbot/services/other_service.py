from feature.chatbot.action.specialty.get_specialties_action import get_specialties_action
import streamlit as st

def get_welcome_message():
    """Mensaje de bienvenida."""
    return (
        "👋 ¡Bienvenido/a al **Estudio Jurídico Camacho Gomez**! \n"
        "Somos un equipo dedicado a ofrecer soluciones legales a tu medida. "
        "Cuenta con nosotros para guiarte en cada paso del proceso legal."
    )

def get_list_options_message():
    """Mensaje para presentar opciones."""
    return (
        "Cuéntanos en qué podemos ayudarte. Aquí están nuestras especialidades, "
        "elige la que mejor se ajuste a tus necesidades:"
    )

def get_interest_query_message():
    """Consulta sobre el área de interés del usuario."""
    return (
        "¿En qué área te gustaría recibir asesoría o agendar una cita? "
        "Selecciona la opción que se ajuste a tu necesidad y coordinaremos una cita. 😊"
    )

def get_service_details_message(service, idx):
    """Despliega detalles del servicio seleccionado."""
    if f"expander_{idx}" not in st.session_state:
        st.session_state[f"expander_{idx}"] = False

    with st.expander(f"⭐ **Opcion: {idx+1}** {service.nombre_servicio}", expanded=st.session_state[f"expander_{idx}"]):
        st.markdown(f"👨‍⚖️ **Abogado**: {service.nombre_usuario}")
        st.markdown(f"📄 **Descripción**: {service.descripcion_servicio}")
        st.markdown(f"💰 **Precio**: ${service.precio_servicio}")
        st.markdown("Si te interesa, **¡contáctanos para agendar tu cita!** 😊")
        st.session_state[f"expander_{idx}"] = not st.session_state[f"expander_{idx}"]

def get_specialties_message():
    """Lista las especialidades disponibles."""
    specialties = get_specialties_action()
    return "\n".join(
        [f"{index}. **{specialty.name}**: {specialty.description}" 
         for index, specialty in enumerate(specialties, start=1)]
    )
