from pydantic import BaseModel, EmailStr, field_validator, ConfigDict

from src.database.validators import accounts as accounts_validators

# ===================================================================
#                       Base & Common Schemas
# ===================================================================


class BaseEmailPasswordSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        return value.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return accounts_validators.validate_password_strength(value)


class MessageResponseSchema(BaseModel):
    message: str


# ===================================================================
#                       User & Auth Schemas
# ===================================================================


class UserRegistrationRequestSchema(BaseEmailPasswordSchema):
    pass


class UserRegistrationResponseSchema(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserActivationRequestSchema(BaseModel):
    token: str


class UserLoginRequestSchema(BaseEmailPasswordSchema):
    pass


class UserLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ===================================================================
#                       Password Reset Schemas
# ===================================================================


class PasswordResetRequestSchema(BaseModel):
    email: EmailStr


class PasswordResetCompleteRequestSchema(BaseEmailPasswordSchema):
    token: str


# ===================================================================
#                       Token Refresh Schemas
# ===================================================================


class TokenRefreshRequestSchema(BaseModel):
    refresh_token: str


class TokenRefreshResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
