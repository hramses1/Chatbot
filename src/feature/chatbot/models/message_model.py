from pydantic import BaseModel

class MessageModel(BaseModel):
    sender: str
    text: str