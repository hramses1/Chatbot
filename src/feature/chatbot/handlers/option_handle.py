import streamlit as st
from feature.chatbot.services.other_service import SERVICE_SELECTION_MESSAGE
from feature.chatbot.services.services_service import classify_selection_service, classify_servicies, format_service_details


def handle_option_selection(responses: list):
    """Maneja la selección del usuario para las opciones."""
        # Intentar obtener los valores desde classify_selection_service()
    result, is_result_valid = classify_selection_service()

    # Verificar si el servicio retornado es válido y no está vacío
    if not is_result_valid or not result:
        responses.append(
                "⚠️ Lo siento, en este momento no hay servicios disponibles para la especialidad seleccionada."
        )
        st.session_state["awaiting_option_selection"] = False
        return

        # Si result es un diccionario con información del servicio
    if isinstance(result, dict):
        confirmation_message = SERVICE_SELECTION_MESSAGE.format(
            nombre_usuario=result["nombre_usuario"],
            nombre_servicio=result["nombre_servicio"],
        )
        responses.append(confirmation_message)
        st.session_state["awaiting_confirmation"] = True
        st.session_state["awaiting_option_selection"] = False
        return

    # Si result es una lista, obtener el número de servicios disponibles
    if isinstance(result, list):
        max_options = len(result)
    else:
        responses.append(
            "⚠️ Error interno: No se pudieron obtener las opciones. Inténtalo de nuevo más tarde."
        )
        return

    service_details = format_service_details(result)

    if service_details:
        st.session_state["awaiting_confirmation"] = True
        st.session_state["awaiting_option_selection"] = False
            # Enviar el mensaje personalizado utilizando SERVICE_SELECTION_MESSAGE
        confirmation_message = SERVICE_SELECTION_MESSAGE.format(
            nombre_usuario=service_details["nombre_usuario"],
            nombre_servicio=service_details["nombre_servicio"],
        )
        responses.append(confirmation_message)
        responses.append(
        "🎉 Opción seleccionada correctamente. ¿Te gustaría confirmar esta cita?")
        return
    else:
        # Si la opción está fuera del rango, volver a mostrar la lista de servicios
        responses.append(
            f"⚠️ La opción {result} no es válida. Por favor, selecciona una opción entre 1 y {max_options}."
        )
        responses.append("🔄 Mostrando nuevamente los servicios disponibles:")
        data = st.session_state.get("area")
    if data:
        classify_servicies(
            data
        )  # Volver a mostrar los servicios disponibles
    else:
            # Si el formato de la entrada es incorrecto, volver a mostrar los servicios
        responses.append(
            "⚠️ No entendí tu selección. Por favor, utiliza el formato 'Opción 1', 'Opción 2', etc."
        )
        responses.append("🔄 Mostrando nuevamente los servicios disponibles:")
        data = st.session_state.get("area")
        if data:
            classify_servicies(data)