from feature.chatbot.utils.json_utils import load_keywords


def detect_intent(user_input: str) -> str:
    """Detecta la intención del usuario basada en su entrada."""
    # Cargar palabras clave desde el JSON
    keywords = load_keywords("stopwords.json")

    # Extraer palabras clave
    schedule_keywords = keywords.get("schedule_keywords", [])
    review_keywords = keywords.get("review_keywords", [])

    # Buscar palabras clave en la entrada del usuario
    if any(keyword in user_input for keyword in schedule_keywords):
        return "schedule_appointment"
    if any(keyword in user_input for keyword in review_keywords):
        return "review_cases"

    return None