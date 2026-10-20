from pydantic import BaseModel, ValidationError
from pydantic import EmailStr
from uuid import UUID

class CreateClientDTO(BaseModel):
    name: str 
    email: EmailStr
    phone_number: str


class ClientDTO(BaseModel):
    id: UUID
    name: str 
    email: EmailStr
    phone_number: str



