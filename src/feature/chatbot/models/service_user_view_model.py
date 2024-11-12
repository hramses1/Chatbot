from typing import Optional
from pydantic import BaseModel

class ServiceUserViewModel(BaseModel):
    collectionId: Optional[str] = None  # Identificador de la colección
    collectionName: Optional[str] = None  # Nombre de la colección
    id: Optional[str] = None  # Identificador del registro
    id_usuario: Optional[str] = None  # Identificador del usuario
    nombre_usuario: Optional[str] = None  # Nombre del usuario
    genero_usuario: Optional[str] = None  # Género del usuario
    correo_usuario: Optional[str] = None  # Correo electrónico del usuario
    id_servicio: Optional[str] = None  # Identificador del servicio
    nombre_servicio: Optional[str] = None  # Nombre del servicio
    descripcion_servicio: Optional[str] = None  # Descripción del servicio
    id_especialidad: Optional[str] = None  # Identificador de la especialidad
    precio_servicio: Optional[float] = None  # Precio del servicio
    horario_inico: Optional[str] = None  # Hora de inicio del servicio (formato "HH:mm")
    horario_fin: Optional[str] = None  # Hora de fin del servicio (formato "HH:mm")
    horario_usuario: Optional[dict] = None  # Horario completo del usuario
    tiempo_consulta: Optional[int] = None  # Tiempo de consulta en minutos

    class Config:
        orm_mode = True
