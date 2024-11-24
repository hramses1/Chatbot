import streamlit as st

from feature.chatbot.view.form_user import activate_form_user

def handle_user_confirmation(user_input, responses: list):
        """Maneja la confirmación del usuario para agendar la cita."""
        if user_input in ["sí", "si", "s", "yes"]:
            responses.append(
                "🎉 ¡Perfecto! Agenda confirmada. Completa el formulario a continuación."
            )
            activate_form_user()
            st.session_state["show_form_user"] = True
            st.session_state["awaiting_confirmation"] = False
            st.rerun()
        elif user_input in ["no", "n", "not now", "nope"]:
            responses.append(
                "👍 Entendido. Si necesitas algo más, aquí estamos para ayudarte."
            )
            st.session_state["awaiting_confirmation"] = False
        else:
            responses.append(
                "⚠️ No entendí tu respuesta. Por favor, responde con 'sí' o 'no'."
            )