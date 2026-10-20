from concurrent import futures
import uuid

import logging
import grpc

import gateway.rpc.contracts.orders_pb2_grpc as orders_pb2_grpc
import gateway.rpc.contracts.orders_pb2 as orders_pb2

from orders.db import get_session
from orders.dto import CreateClientDTO
from orders.repository.client_repository import ClientRepository
from orders.services import ClientService

logging.basicConfig(level=logging.INFO)


class ClientServicer(orders_pb2_grpc.ClientServiceServicer): 
    def __init__(self, domain_service: ClientService):
        self.service = domain_service

    def CreateClient(self, request, context):
        logging.info(f"RCP_SERVER: Recieved a create request. Fields: name={request.name}, email={request.email}, phone_number={request.phone_number}")

        client = self.service.create_client(client_dto=CreateClientDTO(name=request.name, email=request.email, phone_number=request.phone_number))
        logging.critical(f"RCP_SERVER: Recieved a client model from domain service: id={client.id}")

        response = orders_pb2.ClientResponse(id=client.id.bytes, name=client.name, email=client.email, phone_number=client.phone_number)
        logging.info(f"RCP_SERVER: Sent a response. Client created. New client`s ID: {response.id}")

        return response


def serve(): 
    server = grpc.server(futures.ThreadPoolExecutor())
    orders_pb2_grpc.add_ClientServiceServicer_to_server(ClientServicer(ClientService(ClientRepository(session_factory=get_session))), server)

    server.add_insecure_port("[::]:50058")
    server.start()
    logging.info(f"Server started. Waiting for requests...")
    
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    