from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import auth
from app.core.config import Settings
from app.db.database import get_db_session
from app.models.account import User
from app.schemas.account import AccountResponse, AccountRegister, LoginResponse

router = APIRouter(
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not found"}
    }
)


@router.post("/account_register", response_model=AccountResponse)
async def register_account(
        name: str = Form(..., description="Account name"),
        email: str = Form(..., description="Account email"),
        password: str = Form(..., description="Account password"),
        session: AsyncSession = Depends(get_db_session),
):
    try:
        account = AccountRegister(name=name, email=email, password=password)
    except ValueError as e:
        raise HTTPException(detail=str(e))

    async with session.begin():
        new_item = User(
            name=account.name,
            email=account.email,
            hashed_password=auth.get_password_hash(account.password)
        )
        session.add(new_item)
        await session.commit()

    return {
        "name": account.name,
        "email": account.email,
    }


@router.post("/token", response_model=LoginResponse)
async def authorization(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db_session),
):
    account = await auth.get_account_by_email_or_name(
        db, email=form_data.username, name=form_data.username
    )

    if not account or not auth.verify_password(form_data.password, account.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
