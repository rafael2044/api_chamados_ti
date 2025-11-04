from fastapi import Request, HTTPException, status
from sqlalchemy.exc import OperationalError

async def db_connection_exception_handler(request: Request, exc: OperationalError):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="O serviço de banco de dados está indisponível. Tente novamente!"
    )