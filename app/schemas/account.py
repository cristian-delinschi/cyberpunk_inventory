from pydantic import BaseModel


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class AccountResponse(BaseModel):
    name: str
    email: str
    password: str


class AccountRegister(BaseModel):
    name: str
    email: str
