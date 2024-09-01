from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.models.account import User
from app.core.auth import get_password_hash, get_account_by_email_or_name, verify_password, \
    create_access_token
from app.core.config import Settings
from app.schemas.account import AccountRegister, LoginResponse

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/account_register", response_model=AccountRegister)
async def register_account(
        name: str, email: str, password: str,
        session: AsyncSession = Depends(get_db_session),
):
    async with session.begin():
        new_item = User(
            name=name,
            email=email,
            hashed_password=get_password_hash(password)
        )
        session.add(new_item)
        await session.commit()

    return {"name": name}


@router.post("/token", response_model=LoginResponse)
async def authorization(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db_session),
):
    account = await get_account_by_email_or_name(db, email=form_data.username, name=form_data.username)

    if not account or not verify_password(form_data.password, account.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
