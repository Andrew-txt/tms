from concurrent import futures
import uuid

import logging
import grpc

import contracts.orders_pb2_grpc as orders_pb2_grpc
import contracts.orders_pb2 as orders_pb2

logging.basicConfig(level=logging.INFO)


class ClientServicer(orders_pb2_grpc.ClientServiceServicer): 
    def CreateClient(self, request, context):
        logging.info(f"Recieved a create request. Fields: name={request.name}, email={request.name}, phone_number={request.phone_number}")

        response = orders_pb2.ClientResponse(id=uuid.uuid4().bytes, name=request.name, email=request.email, phone_number=request.phone_number)
        logging.info(f"Sent a response. Client created. New client`s ID: {response.id}")

        return response


def serve(): 
    server = grpc.server(futures.ThreadPoolExecutor())
    orders_pb2_grpc.add_ClientServiceServicer_to_server(ClientServicer(), server)

    server.add_insecure_port("[::]:50053")
    server.start()
    logging.info(f"Server started. Waiting for requests...")
    
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    