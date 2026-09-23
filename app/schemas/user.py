from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

from datetime import datetime

class RegisterForm(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)


    model_config = ConfigDict(
        extra="forbid"
    )

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        allowed_symbols = {" ", "-", "'"}

        for char in value:
            if not char.isalpha() and char not in allowed_symbols:
                raise ValueError(
                    "Name can contain only letters, spaces, hyphens and apostrophes"
                )

        return value

class VerifyEmailForm(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)

class LoginForm(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    model_config = ConfigDict(extra="forbid")

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ResendVerificationCodeForm(BaseModel):
    email: EmailStr