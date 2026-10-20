from enum import StrEnum, auto
from uuid import UUID, uuid4

from orders.domain.cargo import Cargo

class OrderStatus(StrEnum):
    UNCOORDINATED = auto()
    EN_ROUTE = auto()
    DELIVERED = auto()
    

class Order: # доменная модель "Клиент"
    def __init__(self, id: UUID = None , cargo_id: UUID = None , client_id: UUID = None):
        self.id = id
        self.cargo_id = cargo_id
        self.client_id = client_id
        self.status = OrderStatus.UNCOORDINATED


    @classmethod
    def create_order(cls, cargo_id: UUID, client_id: UUID) -> Order:
        return cls(uuid4(), cargo_id, client_id)

    
    def switch_status(self) -> bool:
        available_statuses = {
            OrderStatus.UNCOORDINATED: OrderStatus.EN_ROUTE, 
            OrderStatus.EN_ROUTE: OrderStatus.DELIVERED
        }

        new_status = available_statuses.get(self.status)

        if new_status:
            self.status = new_status
            return True
        
        elif not new_status:
            return False
