from feature.chatbot.view.form_email import activate_form_email
import streamlit as st

def handle_case_review() -> list:
    """Maneja la lógica para revisar casos pendientes."""
    print("Aquí pon lo que quieres hacer cuando el usuario escoja revisar casos pendientes.")
    # Ejemplo de lógica personalizada:
    cases = [
        {"id": 1, "status": "Pendiente", "description": "Caso sobre derecho penal"},
        {"id": 2, "status": "Resuelto", "description": "Caso de asesoría laboral"},
    ]
    # Generar una respuesta para el usuario
    responses = ["🔍 Aquí están tus casos pendientes:"]
    for case in cases:
        activate_form_email()
        st.session_state["awaiting_confirmation"] = False
        st.rerun()
        responses.append(f"- Caso ID: {case['id']}, Estado: {case['status']}, Descripción: {case['description']}")
    return responses
