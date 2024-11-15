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

        # Verificar si el formulario fue enviado y obtener datos
        if st.session_state.get("form_submitted", False):
            form_data = get_form_data_user()
            if self.validate_form_data(form_data):
                responses.append(
                    f"🎉 ¡Gracias, {form_data['nombre']}! Hemos recibido tu información correctamente."
                )
                responses.append(f"📧 Email: {form_data['email']}")
                responses.append(f"🆔 Identificación: {form_data['id']}")
                save_to_json(form_data)
                st.session_state["form_submitted"] = False
                st.session_state["show_form_user"] = False
                return {"responses": responses, "activate_form": False}
            else:
                responses.append(
                    "⚠️ Algunos datos son incorrectos. Asegúrate de que tu nombre solo contenga letras, tu email sea válido y tu identificación solo contenga números."
                )
                st.session_state["form_submitted"] = False
                st.session_state["show_form_user"] = True
                return {"responses": responses, "activate_form": True}

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

    def validate_form_data(self, form_data: dict) -> bool:
        """Valida los datos del formulario."""
        if not form_data:
            return False
        if not form_data.get("nombre") or not re.match(
            r"^[a-zA-Z\s]+$", form_data["nombre"]
        ):
            return False
        if not form_data.get("email") or not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", form_data["email"]
        ):
            return False
        if not form_data.get("id") or not form_data["id"].isdigit():
            return False
        return True

    def handle_classification(self, responses: list):
        """Clasifica la entrada del usuario en especialidades."""
        specialty, is_specialty_valid = classify_specialties(self.user_input)

        if is_specialty_valid:
            self.handle_specialty(specialty, responses)
        else:
            responses.append(
                "❌ En este momento no hay especialidad disponible que coincida con tu solicitud. Es posible que hayas escrito algo incorrecto. Por favor, revisa tu petición y vuelve a intentarlo. Ejemplo: 'Derecho Penal'."
            )
    def handle_specialty(self, specialty: str, responses: list):
        """Maneja la respuesta si se detecta una especialidad válida."""
        classify_servicies(specialty)
        save_to_json({"area": specialty})
        st.session_state["area"] = specialty  # Guardar el área en session_state
        responses.append("🔍 Hemos identificado tu interés en una especialidad.")
        responses.append(
            "✅ Por favor, selecciona una opción para continuar. Ejemplo: 'Opción 1', 'Opción 2'."
        )
        st.session_state["awaiting_option_selection"] = True

    def handle_option_selection(self, responses: list):
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

        # Si `result` es un diccionario con información del servicio
        if isinstance(result, dict):
            confirmation_message = SERVICE_SELECTION_MESSAGE.format(
                nombre_usuario=result["nombre_usuario"],
                nombre_servicio=result["nombre_servicio"],
            )
            responses.append(confirmation_message)
            st.session_state["awaiting_confirmation"] = True
            st.session_state["awaiting_option_selection"] = False
            return

        # Si `result` es una lista, obtener el número de servicios disponibles
        if isinstance(result, list):
            max_options = len(result)
            selection = result
        else:
            responses.append(
                "⚠️ Error interno: No se pudieron obtener las opciones. Inténtalo de nuevo más tarde."
            )
            return

        # Validar la entrada del usuario
        match = re.search(r"opci[oó]n\s*(\d+)", self.user_input)
        if match:
            selected_option = int(match.group(1))

            # Verificar si la opción seleccionada está dentro del rango válido
            if 1 <= selected_option <= max_options:
                selected_service = selection[selected_option - 1]
                service_details = format_service_details(selected_service)

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
                        "🎉 Opción seleccionada correctamente. ¿Te gustaría confirmar esta cita?"
                    )
                    return
            else:
                # Si la opción está fuera del rango, volver a mostrar la lista de servicios
                responses.append(
                    f"⚠️ La opción {selected_option} no es válida. Por favor, selecciona una opción entre 1 y {max_options}."
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

    def handle_user_confirmation(self, responses: list):
        """Maneja la confirmación del usuario para agendar la cita."""
        if self.user_input in ["sí", "si", "s", "yes"]:
            responses.append(
                "🎉 ¡Perfecto! Agenda confirmada. Completa el formulario a continuación."
            )
            activate_form_user()
            st.session_state["show_form_user"] = True
            st.session_state["awaiting_confirmation"] = False
            st.rerun()
        elif self.user_input in ["no", "n", "not now", "nope"]:
            responses.append(
                "👍 Entendido. Si necesitas algo más, aquí estamos para ayudarte."
            )
            st.session_state["awaiting_confirmation"] = False
        else:
            responses.append(
                "⚠️ No entendí tu respuesta. Por favor, responde con 'sí' o 'no'."
            )
