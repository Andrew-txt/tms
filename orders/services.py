import logging
import uuid

from orders.domain.client import Client
from orders.dto import ClientDTO, CreateClientDTO
from orders.models import SQLAlchemyClient
from orders.repository.client_repository import ClientRepository

logging.basicConfig(level=logging.INFO)

class ClientService:
    def __init__(self, client_repository: ClientRepository):
        self.repository = client_repository

    def create_client(self, client_dto: CreateClientDTO) -> ClientDTO:
        logging.info(f"DOMAIN_CLIENT_SERVICE: Creating a client...")
        client = Client.create(id=uuid.uuid4(), name=client_dto.name, email=client_dto.email, phone_number=client_dto.email)

        self.repository.create_client(client)
        logging.info(f"DOMAIN_CLIENT_SERVICE: Added the client to repo.")
        return ClientDTO(**client.to_mapping())


        