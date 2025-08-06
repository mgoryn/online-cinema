from datetime import date
from typing import Optional

from fastapi import HTTPException, UploadFile, Form, File
from pydantic import BaseModel, field_validator, HttpUrl, ConfigDict

# Виправлено шлях імпорту
from src.validation import profile as profile_validators
from src.database.models.accounts import GenderEnum


class ProfileCreateSchema(BaseModel):
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str
    avatar: UploadFile

    @classmethod
    def from_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        gender: str = Form(...),
        date_of_birth: date = Form(...),
        info: str = Form(...),
        avatar: UploadFile = File(...),
    ) -> "ProfileCreateSchema":
        return cls(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            info=info,
            avatar=avatar,
        )

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name_field(cls, name: str) -> str:
        try:
            profile_validators.validate_name(name)
            return name.title()  # Робимо першу літеру великою
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    @field_validator("avatar")
    @classmethod
    def validate_avatar(cls, avatar: UploadFile) -> UploadFile:
        try:
            profile_validators.validate_image(avatar)
            return avatar
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    @field_validator("gender")
    @classmethod
    def validate_gender_field(cls, gender: str) -> str:
        try:
            profile_validators.validate_gender(gender)
            return gender
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, date_of_birth: date) -> date:
        try:
            profile_validators.validate_birth_date(date_of_birth)
            return date_of_birth
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    @field_validator("info")
    @classmethod
    def validate_info(cls, info: str) -> str:
        cleaned_info = info.strip()
        if not cleaned_info:
            raise HTTPException(
                status_code=422,
                detail="Info field cannot be empty or contain only spaces.",
            )
        return cleaned_info


class ProfileResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    first_name: str
    last_name: str
    gender: GenderEnum
    date_of_birth: date
    info: str
    avatar: HttpUrl


class ProfileUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    info: Optional[str] = None
