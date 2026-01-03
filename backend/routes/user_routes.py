from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserOut, UserLogin, Token
from services.user_service import UserService
from utils.deps import get_current_user, get_session
from models.user import User
import bcrypt

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    service = UserService(session)
    existing_user = await service.repo.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    user = user.model_copy(update={"password": hashed_password})
    db_user = User(**user.model_dump())
    user = await service.repo.add_user(db_user)
    return UserOut.model_validate(user)


@router.post("/login", response_model=Token)
async def login_user(
    user_credentials: UserLogin, session: AsyncSession = Depends(get_session)
):
    service = UserService(session)
    user = await service.authenticate_user(user_credentials)
    access_token = service.create_access_token(sub=user["username"])
    return Token(access_token=access_token)


@router.get("/me", response_model=UserOut)
async def read_current_user(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    user = await service.repo.get_user_by_username(current_user["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user)
