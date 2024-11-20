from typing import Any, Dict

from feature.chatbot.api.appointment_api import (
    create_appointment,
    create_appointment_detail,
)

def create_appointment_with_detail(
    appointment_data: Dict[str, Any], detail_data: Dict[str, Any]
) -> bool:
    """
    Crea una cita y su detalle de forma secuencial.
    """
    # Crear la cita
    appointment = create_appointment(appointment_data)
    if not appointment:
        print("⚠️ No se pudo crear la cita.")
        return False

    # Agregar el ID de la cita al detalle
    detail_data["cita"] = appointment.id

    # Crear el detalle de la cita
    detail = create_appointment_detail(detail_data)
    if not detail:
        print("⚠️ No se pudo crear el detalle de la cita.")
        return False

    print("✅ Cita y detalle creados exitosamente.")
    return True
