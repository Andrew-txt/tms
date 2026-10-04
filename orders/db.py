import os
from typing import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from pydantic_settings import BaseSettings 
from dotenv import load_dotenv


def create_engine_from_env() -> Engine:
    load_dotenv()
    return create_engine(
        f"sqlite:///{os.getenv('DATABASE_NAME')}",
        connect_args={"check_same_thread": False},
    )


def create_sessionmaker(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


engine = create_engine_from_env()
SessionLocal = create_sessionmaker(engine)


def get_session() -> Iterator[Session]:  # TODO?: в чем разница между Generator и Iterator?
    session = SessionLocal()

    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()

        
        


