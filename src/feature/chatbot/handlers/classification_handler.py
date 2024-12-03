from config.config import USE_AI
from feature.chatbot.handlers.specialty_handle import handle_specialty_selection
from feature.chatbot.services.specialty_service import classify_specialties, classify_specialties_ai

def handle_classification(user_input,responses: list):
    """Clasifica la entrada del usuario en especialidades."""

    if USE_AI == "True":
        specialty, is_specialty_valid = classify_specialties_ai(user_input)
    else:
        specialty, is_specialty_valid = classify_specialties(user_input)
     
    print(specialty, is_specialty_valid)
    if is_specialty_valid:
        handle_specialty_selection(specialty, responses)
    else:
        responses.append(
            "❌ En este momento no hay especialidad disponible que coincida con tu solicitud. Es posible que hayas escrito algo incorrecto. Por favor, revisa tu petición y vuelve a intentarlo. Ejemplo: 'Derecho Penal'."
        )
