from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CustomerModel(BaseModel):
    id: Optional[str] = None  # Identificador del usuario (15 caracteres, generado automáticamente si no se establece)
    nombre: Optional[str] = None  # Nombre del usuario (texto plano)
    identificacion: Optional[str] = None  # Identificación del usuario (texto plano)
    correo: Optional[EmailStr] = None  # Correo electrónico del usuario (dirección de correo válida)
    correo_verificado: Optional[bool] = False  # Si el correo ha sido verificado
    activo: Optional[bool] = True  # Define si el usuario está activo
    usuario_crea_id: Optional[str] = None  # ID del usuario que crea este registro
    usuario_actualiza_id: Optional[str] = None  # ID del usuario que actualiza este registro
    borrado: Optional[bool] = False  # Define si el registro está marcado como eliminado
    creado_en: Optional[datetime] = None  # Fecha de creación
    actualizado_en: Optional[datetime] = None  # Fecha de última actualización

    class Config:
        orm_mode = True
