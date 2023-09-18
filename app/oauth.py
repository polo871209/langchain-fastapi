from typing import Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlmodel import select

from app.database import GetAsyncSession
from app.models import ApiKey
from app.utils.hash import verify_key

# API Key header name
api_key_header = APIKeyHeader(name="X-API-Key")


async def get_api_key(
    session: GetAsyncSession, key: str = Security(api_key_header)
) -> str:
    """verify and return an API key"""
    get_api_keys_stmt = select(ApiKey.api_key)
    api_keys = await session.exec(get_api_keys_stmt)

    for api_key in api_keys.all():
        if verify_key(key, api_key):
            return key

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
    )


ApiAuth = Annotated[str, Security(get_api_key)]
