from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session


def get_session():
    from app import db
    engine = db.engine
    session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
    return session


@contextmanager
def transaction_scope(session):
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
