from pydantic import BaseModel
from typing import Optional
from datetime import date


class SignUpRequestModel(BaseModel):
    username: str
    password: str
