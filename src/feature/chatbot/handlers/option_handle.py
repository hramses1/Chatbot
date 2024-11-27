import streamlit as st
from feature.chatbot.services.other_service import SERVICE_SELECTION_MESSAGE
from feature.chatbot.services.services_service import classify_selection_service, classify_servicies, format_service_details
from feature.chatbot.utils.json_utils import get_all_data_from_json


def handle_option_selection(responses: list):
    """
    Maneja la selección del usuario para las opciones disponibles.

    Args:
        responses (list): Lista donde se almacenan las respuestas para mostrar al usuario.
    """
    try:
        # Obtener valores desde classify_selection_service()
        result, is_result_valid = classify_selection_service()

        # Validación inicial: Revisar si hay un resultado válido
        if not is_result_valid or not result:

            responses.append("🔄 Por favor, intenta seleccionar nuevamente.")
            
            # Lógica de reintento: Reasignar el estado para permitir nueva selección
            st.session_state["awaiting_option_selection"] = True

            # Volver a mostrar las opciones si `area` está disponible
            export_area=get_all_data_from_json()
            data = export_area.get("area")
            if data:
                responses.append("🔄 Mostrando nuevamente los servicios disponibles:")
                classify_servicies(data)
            else:
                responses.append(
                    "⚠️ No entendí tu selección. Por favor, utiliza el formato 'Opción 1', 'Opción 2', etc."
                )
            return

        # Si result es un diccionario, manejar la confirmación
        if isinstance(result, dict):
            confirmation_message = SERVICE_SELECTION_MESSAGE.format(
                nombre_usuario=result["nombre_usuario"],
                nombre_servicio=result["nombre_servicio"],
            )
            responses.append(confirmation_message)
            st.session_state["awaiting_confirmation"] = True
            st.session_state["awaiting_option_selection"] = False
            return

        # Si result es una lista, procesar las opciones disponibles
        if isinstance(result, list):
            service_details = format_service_details(result)

            if service_details:
                confirmation_message = SERVICE_SELECTION_MESSAGE.format(
                    nombre_usuario=service_details["nombre_usuario"],
                    nombre_servicio=service_details["nombre_servicio"],
                )
                responses.append(confirmation_message)
                st.session_state["awaiting_confirmation"] = True
                st.session_state["awaiting_option_selection"] = False
                return
            else:
                responses.append(
                    "⚠️ No se encontraron detalles válidos para los servicios seleccionados. Por favor, selecciona nuevamente."
                )
                st.session_state["awaiting_option_selection"] = True
                return

        # Si el formato de result es inválido
        responses.append(
            "⚠️ Error interno: No se pudieron obtener las opciones. Inténtalo de nuevo más tarde."
        )
        st.session_state["awaiting_option_selection"] = True

    except Exception as e:
        # Manejo de errores inesperados
        responses.append("⚠️ Ha ocurrido un error inesperado. Por favor, inténtalo nuevamente.")
        responses.append(f"🔧 Detalles del error: {str(e)}")
        st.session_state["awaiting_option_selection"] = True
