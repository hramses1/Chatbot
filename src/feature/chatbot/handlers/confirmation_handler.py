import streamlit as st

from feature.chatbot.view.form_user import activate_form_user
import time

def handle_user_confirmation(user_input, responses: list):
    """
    Maneja la confirmación del usuario para agendar la cita.

    Args:
        user_input (str): Entrada del usuario.
        responses (list): Lista donde se almacenan las respuestas para mostrar al usuario.
    """
    if user_input.lower() in ["sí", "si", "s", "yes"]:
        print('Opcion escogida: Si')
        responses.append(
            "🎉 ¡Perfecto! Agenda confirmada. Completa el formulario a continuación."
        )
        activate_form_user()
        st.session_state["show_form_user"] = True
        st.session_state["awaiting_confirmation"] = False
        st.rerun()

    elif user_input.lower() in ["no", "n", "not now", "nope"]:
        print('Opcion escogida: No')
        responses.append(
            "👍 Entendido. Serás redirigido al inicio. Si necesitas algo más, aquí estamos para ayudarte. 😊"
        )

        # Mostrar el mensaje antes de limpiar el estado
        for response in responses:
            st.info(response)  # Mostrar todas las respuestas
        time.sleep(7)  # Espera para que el usuario lea el mensaje

        # Limpiar estado y redirigir
        st.session_state.clear()
        st.rerun()

    else:
        responses.append(
            "⚠️ No entendí tu respuesta. Por favor, responde con 'sí' o 'no'."
        )
