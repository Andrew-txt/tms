from uuid import UUID, uuid4
import uuid

class Client: # доменная модель "Клиент"
    def __init__(self, id: UUID, name: str, email: str, phone_number: str):
        self.id = id
        self.name = name
        self.email = email
        self.phone_number = phone_number

    @classmethod
    def create(cls, id: UUID,  name: str, email: str, phone_number: str):
        return Client(id=id, name=name, email=email, phone_number=phone_number)

    def to_mapping(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number
        }
