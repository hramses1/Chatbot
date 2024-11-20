from feature.chatbot.services.specialty_service import classify_specialties
from feature.chatbot.view.form_user import activate_form_user, get_form_data_user
from feature.chatbot.services.services_service import (
    classify_selection_service,
    classify_servicies,
    format_service_details,
)
from feature.chatbot.utils.json_utils import save_to_json
from feature.chatbot.services.other_service import SERVICE_SELECTION_MESSAGE
import streamlit as st
import re

class MessageService:
    def __init__(self, user_input: str):
        self.user_input = user_input.lower().strip()

    def create_user_message(self) -> dict:
        """Crea y devuelve un mensaje de usuario."""
        return {"sender": "user", "text": self.user_input}

    def generate_multiple_responses(self) -> dict:
        """Genera respuestas del bot y devuelve un diccionario."""
        responses = []

        # Manejo del formulario enviado
        if st.session_state.get("form_submitted", False):
            self.process_form_submission(responses)
            return {"responses": responses, "activate_form": st.session_state["show_form_user"]}

        # Clasificación de la entrada del usuario
        if st.session_state.get("awaiting_confirmation", False):
            self.handle_user_confirmation(responses)
        elif st.session_state.get("awaiting_option_selection", False):
            self.handle_option_selection(responses)
        else:
            self.handle_classification(responses)

        return {
            "responses": responses,
            "activate_form": st.session_state.get("show_form_user", False),
        }

    def process_form_submission(self, responses: list):
        """Procesa el envío del formulario."""
        form_data = get_form_data_user()
        if self.validate_form_data(form_data):
            responses.append(f"🎉 ¡Gracias, {form_data['nombre']}! Hemos recibido tu información correctamente.")
            responses.extend([
                f"📧 Email: {form_data['email']}",
                f"🆔 Identificación: {form_data['id']}",
            ])
            save_to_json(form_data)
            self.reset_states("form_submitted", "show_form_user")
        else:
            responses.append(
                "⚠️ Algunos datos son incorrectos. Asegúrate de que tu nombre solo contenga letras, tu email sea válido y tu identificación solo contenga números."
            )
            st.session_state["show_form_user"] = True

    def validate_form_data(self, form_data: dict) -> bool:
        """Valida los datos del formulario."""
        validators = {
            "nombre": lambda x: bool(re.match(r"^[a-zA-Z\s]+$", x)),
            "email": lambda x: bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", x)),
            "id": lambda x: x.isdigit(),
        }
        return all(validators[key](form_data.get(key, "")) for key in validators)

    def handle_classification(self, responses: list):
        """Clasifica la entrada del usuario en especialidades."""
        specialty, is_specialty_valid = classify_specialties(self.user_input)
        if is_specialty_valid:
            classify_servicies(specialty)
            responses.append("🔍 Hemos identificado tu interés en una especialidad.")
            responses.append("✅ Por favor, selecciona una opción para continuar. Ejemplo: 'Opción 1', 'Opción 2'.")
            st.session_state["awaiting_option_selection"] = True
        else:
            responses.append(
                "❌ No encontramos una especialidad que coincida con tu solicitud. Intenta de nuevo con términos como 'Derecho Penal'."
            )

    def handle_option_selection(self, responses: list):
        """Maneja la selección del usuario para las opciones."""
        result, is_result_valid = classify_selection_service()

        if not is_result_valid or not result:
            responses.append(result)
            st.session_state["awaiting_option_selection"] = False
            return

        if isinstance(result, dict):
            self.prepare_confirmation_message(result, responses)
        elif isinstance(result, list):
            self.process_option_list(result, responses)

    def process_option_list(self, options: list, responses: list):
        """Procesa una lista de opciones disponibles."""
        max_options = len(options)
        match = re.search(r"opci[oó]n\s*(\d+)", self.user_input)
        if match:
            selected_option = int(match.group(1))
            if 1 <= selected_option <= max_options:
                self.prepare_confirmation_message(options[selected_option - 1], responses)
            else:
                responses.append(
                    f"⚠️ La opción {selected_option} no es válida. Por favor, selecciona entre 1 y {max_options}."
                )
        else:
            responses.append("⚠️ Por favor, selecciona una opción válida como 'Opción 1'.")

    def prepare_confirmation_message(self, service_details: dict, responses: list):
        """Prepara un mensaje de confirmación para una opción seleccionada."""
        confirmation_message = SERVICE_SELECTION_MESSAGE.format(
            nombre_usuario=service_details["nombre_usuario"],
            nombre_servicio=service_details["nombre_servicio"],
        )
        responses.append(confirmation_message)
        responses.append("🎉 ¿Te gustaría confirmar esta cita? Responde con 'sí' o 'no'.")
        self.reset_states("awaiting_option_selection")
        st.session_state["awaiting_confirmation"] = True

    def handle_user_confirmation(self, responses: list):
        """Maneja la confirmación del usuario para agendar la cita."""
        if self.user_input in ["sí", "si", "s", "yes"]:
            responses.append("🎉 ¡Perfecto! Agenda confirmada. Completa el formulario a continuación.")
            activate_form_user()
            st.session_state["show_form_user"] = True
        elif self.user_input in ["no", "n", "not now", "nope"]:
            responses.append("👍 Entendido. Si necesitas algo más, aquí estamos para ayudarte.")
        else:
            responses.append("⚠️ No entendí tu respuesta. Por favor, responde con 'sí' o 'no'.")
        self.reset_states("awaiting_confirmation")

    def reset_states(self, *keys):
        """Resetea los estados especificados en session_state."""
        for key in keys:
            st.session_state[key] = False
