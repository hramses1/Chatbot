from pydantic import BaseModel

class SpecialtyModel(BaseModel):
    id: str
    name: str
    description: str