from common.axios import Axios
from feature.chatbot.models.appointment_model import AppointmentModel
from feature.chatbot.models.appointment_detail_model import AppointmentDetailModel
from typing import Any, Dict, Optional


def create_appointment(appointment_data: Dict[str, Any]) -> Optional[AppointmentModel]:
    """
    Crea una cita en la base de datos mediante la API proporcionada.
    """
    response = Axios().post("/collections/cita/records", json=appointment_data)
    if response and "id" in response:
        print("✅ Cita creada exitosamente.")
        return AppointmentModel(**response)
    else:
        print("❌ Error al crear la cita.")
        return None


def create_appointment_detail(
    detail_data: Dict[str, Any]
) -> Optional[AppointmentDetailModel]:
    """
    Crea el detalle de una cita en la base de datos mediante la API proporcionada.
    """
    response = Axios().post("/collections/detalle_cita/records", json=detail_data)
    if response and "id" in response:
        print("✅ Detalle de cita creado exitosamente.")
        return AppointmentDetailModel(**response)
    else:
        print("❌ Error al crear el detalle de la cita.")
        return None
