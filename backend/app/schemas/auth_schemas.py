from pydantic import BaseModel
from datetime import time


class LoginSchema(BaseModel):
    correo: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
