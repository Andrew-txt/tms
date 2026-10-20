from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from orders.db import engine
from orders.domain.cargo import CargoTimeType
from orders.domain.order import OrderStatus

Base = declarative_base()

class SQLAlchemyClient(Base):
    __tablename__ = "client"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] 
    email: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str] = mapped_column(unique=True,  nullable=False)
    orders: Mapped[list["SQLAlchemyOrder"]] = relationship(back_populates="client")


class SQLAlchemyOrder(Base):
    __tablename__ = "order"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    cargo_id: Mapped[UUID] = mapped_column(ForeignKey(column="cargo.id"))
    client_id: Mapped[UUID] = mapped_column(ForeignKey(column="client.id"))
    client: Mapped["SQLAlchemyClient"] = relationship(back_populates="orders") # ?: у клиента ищется поле orders  (ссылка на атрибут order вызывает ошибку sqlalchemy.exc.InvalidRequestError: )
    # Правило такое: back_populates в Order.client = имя атрибута в Client (orders), а back_populates в Client.orders = имя атрибута в Order (client). Они должны быть зеркальными.

    status: Mapped[OrderStatus]


class SQLAlchemyCargo(Base):
    __tablename__ = "cargo"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    time_type: Mapped[CargoTimeType]
    cargo_units: Mapped[list["SQLAlchemyCargoUnit"]] = relationship(back_populates="cargo") 


class SQLAlchemyCargoUnit(Base):
    __tablename__ = "cargo_unit"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    cargo_id: Mapped[UUID] = mapped_column(ForeignKey(column="cargo.id"))
    cargo: Mapped["SQLAlchemyCargo"] = relationship(back_populates="cargo_units")
    length_value: Mapped[int]
    length_unit: Mapped[str]

    width_value: Mapped[int]
    width_unit: Mapped[str]

    height_value: Mapped[int]
    height_unit: Mapped[str]

    weight_value: Mapped[int]
    weight_unit: Mapped[str]


Base.metadata.create_all(bind=engine) # TODO: лучшая практика - перенести в lifespan в main