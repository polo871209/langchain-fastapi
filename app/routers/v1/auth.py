import secrets

from fastapi import APIRouter

from app.database import GetAsyncSession
from app.models import ApiKey
from app.oauth import ApiAuth
from app.utils.hash import get_key_hash

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/")
async def create_key(session: GetAsyncSession, auth: ApiAuth):
    """create new api key"""
    api_key = secrets.token_urlsafe(32)
    hashed_key = get_key_hash(api_key)

    # Store the hashed_key and api_key_id in the database
    new_api_key = ApiKey(api_key=hashed_key)
    session.add(new_api_key)
    await session.commit()

    return {"api_key": api_key}
