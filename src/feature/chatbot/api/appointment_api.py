from common.axios import Axios
from feature.chatbot.models.appointment_model import AppointmentModel
from feature.chatbot.models.appointment_detail_model import AppointmentDetailModel
from typing import Any, Dict, Optional


class AppointmentService:
    def __init__(self):
        self.axios = Axios()

    def create_appointment(self, appointment_data: Dict[str, Any]) -> Optional[AppointmentModel]:
        """
        Crea una cita en la base de datos mediante la API proporcionada.
        """
        response = self.axios.post('/collections/cita/records', json=appointment_data)
        if response and 'id' in response:
            print("✅ Cita creada exitosamente.")
            return AppointmentModel(**response)
        else:
            print("❌ Error al crear la cita.")
            return None

    def create_appointment_detail(self, detail_data: Dict[str, Any]) -> Optional[AppointmentDetailModel]:
        """
        Crea el detalle de una cita en la base de datos mediante la API proporcionada.
        """
        response = self.axios.post('/collections/detalle_cita/records', json=detail_data)
        if response and 'id' in response:
            print("✅ Detalle de cita creado exitosamente.")
            return AppointmentDetailModel(**response)
        else:
            print("❌ Error al crear el detalle de la cita.")
            return None

    def create_appointment_with_detail(self, appointment_data: Dict[str, Any], detail_data: Dict[str, Any]) -> bool:
        """
        Crea una cita y su detalle de forma secuencial.
        """
        # Crear la cita
        appointment = self.create_appointment(appointment_data)
        if not appointment:
            print("⚠️ No se pudo crear la cita.")
            return False

        # Agregar el ID de la cita al detalle
        detail_data['cita'] = appointment.id

        # Crear el detalle de la cita
        detail = self.create_appointment_detail(detail_data)
        if not detail:
            print("⚠️ No se pudo crear el detalle de la cita.")
            return False

        print("✅ Cita y detalle creados exitosamente.")
        return True