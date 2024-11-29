from common.utils import format_message
from typing import List
from feature.chatbot.models.specialty_model import SpecialtyModel

def get_bot_response(user_message):
    # Lógica simple para el chatbot (puede expandirse)
    response = user_message

    return format_message(response)

def build_prompt_specialties(records: List[SpecialtyModel]):
    """Construye el prompt dinámicamente en base a los registros."""
    formatted_records = []
    for record in records:
        formatted_records.append(
            f"id: {record.id} - nombre: {record.name} - descripcion: {record.description}"
        )

    prompt = (
        "Quiero que actúes como un buscador avanzado que encuentra similitudes en una base de datos. "
        "Te proporcionaré una entrada (nombre o una descripción relacionada con un área del derecho). "
        "Tu tarea es identificar el `id` exacto del registro que mejor coincida, ya sea por similitud directa o semántica. "
        "Si no encuentras ninguna coincidencia o si la entrada no tiene sentido, responde con `0`. "
        "Si encuentras una coincidencia, devuelve solo el `id` correspondiente. "
        "No respondas con explicaciones ni detalles adicionales, solo el `id`.\n\n"
        "Estos son los registros disponibles:\n"
        + "\n".join(formatted_records) +
        "\n\nEjemplos de entradas y salidas esperadas:\n\n"
        "- Entrada: \"me robaron el celular\"\n"
        "  Salida: `s4zc1sp29cu08o6`\n\n"
        "- Entrada: \"estacionamiento indebido\"\n"
        "  Salida: `z3n4id2l4yxvmip`\n\n"
        "- Entrada: \"quiero apelar una decisión judicial\"\n"
        "  Salida: `16sgtgey31ev3pg`\n\n"
        "- Entrada: \"contrato laboral injusto\"\n"
        "  Salida: `9gu5icmu4vqekpn`\n\n"
        "- Entrada: \"quiero demandar por daño moral\"\n"
        "  Salida: `0`\n\n"
        "¿Entendiste la tarea? Si estás listo, por favor devuelve el `id` cuando se proporcione un nombre o descripción."
    )
    
    return prompt
