from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    id: str # Identificador del usuario
    username: str # Nombre de usuario
    email: str # Correo electrónico del usuario
    name: str # Nombre del usuario
    gender: str # Género del usuario
    define_schedule: str  # Define si el usuario tiene horario de disponibilidad
    schedule: Optional[str] = None # Horario de disponibilidad
    activo: bool # Define si el usuario está activo