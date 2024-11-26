from typing import Optional, List
from pydantic import BaseModel

class ClienteCasoCorreoItem(BaseModel):
    id: Optional[str] = None  # Identificador del registro
    collectionId: Optional[str] = None  # Identificador de la colección
    collectionName: Optional[str] = None  # Nombre de la colección
    nombre_cliente: Optional[str] = None  # Nombre del cliente
    correo_cliente: Optional[str] = None  # Correo electrónico del cliente
    fecha_cita: Optional[str] = None  # Fecha y hora de la cita (en formato ISO 8601)
    estado_caso: Optional[str] = None  # Estado del caso
    observacion: Optional[str] = None  # Observaciones

    class Config:
        orm_mode = True

class ClienteCasoCorreoResponse(BaseModel):
    page: Optional[int] = None  # Número de página
    perPage: Optional[int] = None  # Elementos por página
    totalPages: Optional[int] = None  # Total de páginas
    totalItems: Optional[int] = None  # Total de elementos
    items: Optional[List[ClienteCasoCorreoItem]] = None  # Lista de elementos

    class Config:
        orm_mode = True
