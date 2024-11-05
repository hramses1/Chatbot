from pydantic import BaseModel

class ServiceModel(BaseModel):
    id: str
    category: str
    name: str
    description: str
    price: int
    status: bool