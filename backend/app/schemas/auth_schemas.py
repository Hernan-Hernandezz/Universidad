from pydantic import BaseModel
from datetime import time


class LoginSchema(BaseModel):
    mail: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
