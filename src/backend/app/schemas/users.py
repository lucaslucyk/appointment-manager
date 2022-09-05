from pydantic import BaseModel, EmailStr, SecretStr


class User(BaseModel):
    email: EmailStr
    password: SecretStr
    is_active: bool
    first_name: str
    last_name: str
    is_professional: bool = False