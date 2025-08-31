from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_engine(url: str) -> Engine:
    """Create a database engine for the given URL."""
    return create_engine(url, future=True)


def get_session(engine: Engine) -> Session:
    """Create a new session bound to the provided engine."""
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)()
