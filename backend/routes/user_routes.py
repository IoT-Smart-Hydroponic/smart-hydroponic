from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas.user import UserCreate, UserOut, UserLogin, Token, UserUpdate
from services.user_service import UserService
from utils.deps import get_current_user, get_session
from models.user import User
from schemas.responses import (
    responses_400,
    responses_401,
    responses_403,
    responses_404,
    responses_500,
)
import bcrypt

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=201,
    operation_id="registerUser",
    responses={
        **responses_400,
        **responses_500,
    },
)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    service = UserService(session)
    try:
        existing_user = await service.get_user_by_username(user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user = user.model_copy(update={"password": hashed_password})
        db_user = User(**user.model_dump())
        user = await service.add_user(db_user)
        return UserOut.model_validate(user)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Username already registered")
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Database error")


@router.post(
    "/login",
    response_model=Token,
    operation_id="loginUser",
    responses={
        **responses_400,
        **responses_401,
        **responses_500,
    },
)
async def login_user(
    user_credentials: UserLogin, session: AsyncSession = Depends(get_session)
):
    service = UserService(session)
    try:
        user = await service.authenticate_user(user_credentials)
        access_token = service.create_access_token(
            data={
                "sub": user.username,
                "id": str(user.userid),
                "role": user.role,
            }
        )
        return Token(access_token=access_token)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@router.get(
    "/me",
    response_model=UserOut,
    operation_id="getCurrentUser",
    responses={
        **responses_401,
        **responses_404,
        **responses_500,
    },
)
async def read_current_user(
    current_user: User = Depends(get_current_user),
):
    try:
        return UserOut.model_validate(current_user)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.get(
    "",
    response_model=list[UserOut],
    operation_id="getAllUsers",
    responses={
        **responses_401,
        **responses_403,
        **responses_500,
    },
)
async def read_users(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    try:
        if current_user.role == "user":
            raise HTTPException(status_code=403, detail="Permission denied")
        users = await service.get_all_users()
        return [UserOut.model_validate(user) for user in users]
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@router.patch(
    "/{user_id}",
    response_model=UserOut,
    operation_id="updateUser",
    responses={
        **responses_400,
        **responses_401,
        **responses_403,
        **responses_404,
        **responses_500,
    },
)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role == "user" and (
        user_update.role == "admin" or user_update.role == "superadmin"
    ):
        raise HTTPException(status_code=403, detail="Permission denied")

    service = UserService(session)
    try:
        updated_user = await service.update_user(user_id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserOut.model_validate(updated_user)

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already registered")
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@router.delete(
    "/{user_id}",
    status_code=200,
    operation_id="deleteUser",
    responses={
        **responses_401,
        **responses_403,
        **responses_404,
        **responses_500,
    },
)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    try:
        if current_user.role == "user":
            raise HTTPException(status_code=403, detail="Permission denied")
        user = await service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user = User(**user)
        await service.delete_user(user)
        return {"detail": "User deleted successfully"}
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Database error")
