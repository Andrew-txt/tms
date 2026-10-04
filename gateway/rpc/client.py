import uuid

import contracts.orders_pb2_grpc as orders_pb2_grpc
import contracts.orders_pb2 as orders_pb2

import logging
import grpc

logging.basicConfig(level=logging.INFO)


def test_conn(host, port):
    logging.info(f"Creating a channel to {host}:{port}")

    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = orders_pb2_grpc.ClientServiceStub(channel)
        logging.info("Sending a request...")

        response = stub.CreateClient(orders_pb2.ClientRequest(name="GreeTestsCo.", email="gree@gmail.com", phone_number="+79011231765" ))

        logging.info(f"Recieved a response from microservice`s rpc server. Client created. New client`s ID in bytes format: {response.id}")


if __name__  == "__main__":
    test_conn("localhost", 50053)