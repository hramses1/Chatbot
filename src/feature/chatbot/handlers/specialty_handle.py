import streamlit as st
from feature.chatbot.services.services_service import classify_servicies
from feature.chatbot.utils.json_utils import save_to_json

def handle_specialty_selection(specialty: str, responses: list):
    """Maneja la respuesta si se detecta una especialidad válida."""
    classify_servicies(specialty)
    save_to_json({"area": specialty})
    st.session_state["area"] = specialty  # Guardar el área en session_state
    responses.append("🔍 Hemos identificado tu interés en una especialidad.")
    responses.append(
        "✅ Por favor, selecciona una opción para continuar. Ejemplo: 'Opción 1', 'Opción 2'."
    )
    st.session_state["awaiting_option_selection"] = True