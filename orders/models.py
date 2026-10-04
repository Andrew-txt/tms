from sqlalchemy.orm import DeclarativeBase
from db import engine

class Base(DeclarativeBase): 
    ...


Base.metadata.create_all(bind=engine) # TODO: лучшая практика - перенести в lifespan в main