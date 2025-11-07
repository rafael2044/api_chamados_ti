from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


from core.settings import Settings

PATH_SSL_ROOT_CERT = Settings().PATH_SSL_ROOT_CERT
PATH_SSL_CERT = Settings().PATH_SSL_CERT
PATH_SSL_KEY = Settings().PATH_SSL_KEY

if (PATH_SSL_ROOT_CERT and PATH_SSL_CERT and PATH_SSL_KEY):
    ssl_args = {
        'sslmode': 'verify-full',
        'sslcert': PATH_SSL_CERT,
        'sslkey': PATH_SSL_KEY,
        'sslrootcert': PATH_SSL_ROOT_CERT
    }

    engine = create_engine(
        Settings().DATABASE_URL,
        connect_args=ssl_args
    )
else:
    engine = create_engine(
        Settings().DATABASE_URL,
    )
    
Base = declarative_base()


def get_session():
    with Session(engine) as session:
        yield session
