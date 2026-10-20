from contextlib import AbstractContextManager
import logging
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from orders.db import get_session
from orders.domain.client import Client
from orders.models import SQLAlchemyClient

logging.basicConfig(level=logging.INFO)


class ClientRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory


    def create_client(self, client: Client) -> Client:
        repo_client = self._from_domain(client)

        with self.session_factory() as session:
            possible_client = session.scalar(select(SQLAlchemyClient).where(SQLAlchemyClient.phone_number==repo_client.phone_number))
            if possible_client:
                logging.info(f"REPOSITORY: Found a possible client: name={possible_client.name}, id={possible_client.id}")
                return self._to_domain(possible_client)
            
            else:
                session.add(repo_client)
                session.commit()
                logging.info(f"REPOSITORY: Added new client. ID: {repo_client.id}")
                return self._to_domain(repo_client)


    def get_client(self, client_id: int) -> Client | None:
        with self.session_factory() as session:
            repo_client = self._get_repo_client(session, client_id)

            if repo_client:
                return self._to_domain(repo_client)
            else:
             return None
       

    def get_client_by_phone_number(self, phone_number: str) -> Client | None:
        with self.session_factory() as session:
            repo_client = session.scalar(select(SQLAlchemyClient).where(SQLAlchemyClient.phone_number == phone_number))
            
            if repo_client:
                return self._to_domain(repo_client)
            else:
                logging.info(f"REPOSITORY: Client with phone_number={phone_number} not found")
                return None
            

    def get_clients(self) -> list[Client]:
        with self.session_factory() as session:
            repo_clients = session.scalars(select(SQLAlchemyClient)).all()
            logging.info(f"REPOSITORY: Fetched {len(repo_clients)} clients")
            return [self._to_domain(repo_client) for repo_client in repo_clients]
        

    def update_client(self, client: Client) -> Client | None:
        with self.session_factory() as session:
            repo_client = self._get_repo_client(session, client.id)
            if repo_client is None:
                return None

            # TODO: подумать над логикой обновления данных пользователя. Как тогда обновлять номер телефона, если понадобится?
            if repo_client.phone_number != client.phone_number:
                conflict = session.scalar(select(SQLAlchemyClient).where(SQLAlchemyClient.phone_number == client.phone_number))

                if conflict is not None:
                    logging.info(f"REPOSITORY: Cannot update client id={client.id}. Phone_number={client.phone_number} already used by id={conflict.id}")
                    return None

            repo_client.name = client.name
            repo_client.email = client.email
            repo_client.phone_number = client.phone_number

            updated_client = self._to_domain(repo_client)
            session.commit()
            logging.info(f"REPOSITORY: Updated client with id={client.id}")
            return updated_client


    def delete_client(self, client_id: int) -> bool:
        with self.session_factory() as session:

            repo_client = self._get_repo_client(session, client_id)
            if repo_client:
                session.delete(repo_client)
                session.commit()
                logging.info(f"REPOSITORY: Deleted client with id={client_id}")
                return True
            else:
                return False


    @staticmethod
    def _to_domain(repo_client: SQLAlchemyClient) -> Client:
        return Client.create(id=repo_client.id, name=repo_client.name, email=repo_client.email, phone_number=repo_client.phone_number)

    @staticmethod
    def _from_domain(domain_client: Client) -> SQLAlchemyClient:
        return SQLAlchemyClient(id=domain_client.id, name=domain_client.name, email=domain_client.email, phone_number=domain_client.phone_number)

    @staticmethod
    def _get_repo_client(session: Session, client_id: int) -> SQLAlchemyClient | None:
        repo_client = session.get(SQLAlchemyClient, client_id)
        if repo_client is None:
            logging.info(f"REPOSITORY: Client with id={client_id} not found")
        return repo_client




