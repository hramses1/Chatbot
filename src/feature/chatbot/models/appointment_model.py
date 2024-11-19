from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentModel(BaseModel):
    id: Optional[str] = None  # Identificador de la cita (15 caracteres, generado automáticamente si no se establece)
    cliente: Optional[str] = None  # Identificador del cliente (relación)
    usuario: Optional[str] = None  # Identificador del abogado asignado (relación)
    estado_caso: Optional[str] = None  # Estado de la cita (P = Pendiente, A = Aprobado, R = Realizada)
    observacion: Optional[str] = None  # Observación del cliente (texto plano)
    fecha_cita: Optional[datetime] = None  # Fecha de la cita

    class Config:
        orm_mode = True
