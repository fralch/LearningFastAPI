from pydantic import BaseModel


class UserModel (BaseModel):
    id: str | None
    username: str
    email: str
