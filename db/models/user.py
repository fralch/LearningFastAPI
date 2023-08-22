from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    id: str = None  # Haciendo que id tenga un valor predeterminado de None
    username: str
    email: str