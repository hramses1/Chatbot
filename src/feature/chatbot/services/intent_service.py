from feature.chatbot.utils.json_utils import load_keywords
from feature.chatbot.utils.json_utils import save_to_json


def detect_intent(user_input: str) -> str:
    """Detecta la intención del usuario basada en su entrada."""
    # Cargar palabras clave desde el JSON
    keywords = load_keywords("stopwords.json")

    # Extraer palabras clave
    schedule_keywords = keywords.get("schedule_keywords", [])
    review_keywords = keywords.get("review_keywords", [])

    # Buscar palabras clave en la entrada del usuario
    if any(keyword in user_input for keyword in schedule_keywords):
        save_to_json({"state_chat":"schedule_appointment"})
        return "schedule_appointment"
    if any(keyword in user_input for keyword in review_keywords):
        save_to_json({"state_chat":"review_cases"})
        return "review_cases"

    return None