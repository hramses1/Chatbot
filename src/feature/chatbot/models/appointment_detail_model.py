from pydantic import BaseModel
from typing import Optional

class AppointmentDetailModel(BaseModel):
    id: Optional[str] = None  # Identificador del detalle de la cita (15 caracteres, generado automáticamente si no se establece)
    cita: Optional[str] = None  # Identificador de la cita (relación)
    servicio: Optional[str] = None  # Identificador del servicio (relación)
    precio: Optional[float] = None  # Precio del servicio (valor numérico)

    class Config:
        orm_mode = True
