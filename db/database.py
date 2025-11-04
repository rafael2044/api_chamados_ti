from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


from core.settings import Settings

ssl_args = {
    'sslmode': 'verify-full',
    'sslcert': Settings().PATH_SSL_CERT,
    'sslkey': Settings().PATH_SSL_KEY,
    'sslrootcert': Settings().PATH_SSL_ROOT_CERT
}

engine = create_engine(
    Settings().DATABASE_URL
)
Base = declarative_base()


def get_session():
    with Session(engine) as session:
        yield session
