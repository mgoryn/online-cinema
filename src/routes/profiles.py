from typing import cast

from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import HttpUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import get_db
from src.config.dependencies import get_s3_storage_client, get_jwt_auth_manager

from src.database.models.accounts import (
    UserModel,
    UserProfileModel,
    UserGroupEnum,
    UserGroupModel,
    GenderEnum,
)
from src.exceptions import S3FileUploadError, BaseSecurityError
from src.schemas.profiles import (
    ProfileResponseSchema,
    ProfileCreateSchema,
    ProfileUpdateSchema,
)
from src.security.http import get_token
from src.security.interfaces import JWTAuthManagerInterface
from src.storages.interfaces import S3StorageInterface


router = APIRouter()


@router.post(
    "/users/{user_id}/profile",
    response_model=ProfileResponseSchema,
    summary="Create user profile",
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    user_id: int,
    token: str = Depends(get_token),
    jwt_manager: JWTAuthManagerInterface = Depends(get_jwt_auth_manager),
    db: AsyncSession = Depends(get_db),  # Оновлена залежність
    s3_client: S3StorageInterface = Depends(get_s3_storage_client),
    profile_data: ProfileCreateSchema = Depends(ProfileCreateSchema.from_form),
) -> ProfileResponseSchema:
    """
    Creates a user profile.
    """
    try:
        payload = jwt_manager.decode_access_token(token)
        token_user_email = payload.get("sub")
        if not token_user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload.",
            )
    except BaseSecurityError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    token_user_stmt = (
        select(UserModel)
        .options(joinedload(UserModel.group))
        .where(UserModel.email == token_user_email)
    )
    token_user_result = await db.execute(token_user_stmt)
    token_user = token_user_result.scalars().first()

    if not token_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User from token not found.",
        )

    if user_id != token_user.id and token_user.group.name != UserGroupEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this profile.",
        )

    target_user_stmt = select(UserModel).where(UserModel.id == user_id)
    target_user_result = await db.execute(target_user_stmt)
    target_user = target_user_result.scalars().first()
    if not target_user or not target_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target user not found or not active.",
        )

    existing_profile_stmt = select(UserProfileModel).where(
        UserProfileModel.user_id == target_user.id
    )
    existing_profile_result = await db.execute(existing_profile_stmt)
    if existing_profile_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a profile.",
        )

    avatar_bytes = await profile_data.avatar.read()
    avatar_key = f"avatars/{target_user.id}_{profile_data.avatar.filename}"

    try:
        await s3_client.upload_file(file_name=avatar_key, file_data=avatar_bytes)
    except S3FileUploadError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload avatar: {e}",
        )

    new_profile = UserProfileModel(
        user_id=cast(int, target_user.id),
        first_name=profile_data.first_name,
        last_name=profile_data.last_name,
        gender=cast(GenderEnum, profile_data.gender),
        date_of_birth=profile_data.date_of_birth,
        info=profile_data.info,
        avatar=avatar_key,
    )

    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)

    avatar_url = await s3_client.get_file_url(new_profile.avatar)

    return ProfileResponseSchema(
        id=new_profile.id,
        user_id=new_profile.user_id,
        first_name=new_profile.first_name,
        last_name=new_profile.last_name,
        gender=new_profile.gender,
        date_of_birth=new_profile.date_of_birth,
        info=new_profile.info,
        avatar=cast(HttpUrl, avatar_url),
    )


@router.get(
    "/users/{user_id}/profile",
    response_model=ProfileResponseSchema,
    summary="Get user profile",
)
async def get_profile(
    user_id: int,
    db: AsyncSession = Depends(get_db),  # Оновлена залежність
    s3_client: S3StorageInterface = Depends(get_s3_storage_client),
) -> ProfileResponseSchema:
    """
    Retrieves a user's profile information.
    """
    stmt = select(UserProfileModel).where(UserProfileModel.user_id == user_id)
    result = await db.execute(stmt)
    profile = result.scalars().first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found for this user.",
        )

    avatar_url = await s3_client.get_file_url(profile.avatar)

    return ProfileResponseSchema(
        id=profile.id,
        user_id=profile.user_id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        gender=profile.gender,
        date_of_birth=profile.date_of_birth,
        info=profile.info,
        avatar=cast(HttpUrl, avatar_url),
    )


@router.patch(
    "/users/{user_id}/profile",
    response_model=ProfileResponseSchema,
    summary="Update user profile",
)
async def update_profile(
    user_id: int,
    profile_data: ProfileUpdateSchema,
    token: str = Depends(get_token),
    jwt_manager: JWTAuthManagerInterface = Depends(get_jwt_auth_manager),
    db: AsyncSession = Depends(get_db),  # Оновлена залежність
    s3_client: S3StorageInterface = Depends(get_s3_storage_client),
) -> ProfileResponseSchema:
    """
    Updates a user's profile information.
    """
    try:
        payload = jwt_manager.decode_access_token(token)
        token_user_email = payload.get("sub")
    except BaseSecurityError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    token_user_stmt = (
        select(UserModel)
        .options(joinedload(UserModel.group))
        .where(UserModel.email == token_user_email)
    )
    token_user_result = await db.execute(token_user_stmt)
    token_user = token_user_result.scalars().first()

    if not token_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User from token not found.",
        )

    if user_id != token_user.id and token_user.group.name != UserGroupEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this profile.",
        )

    stmt = select(UserProfileModel).where(UserProfileModel.user_id == user_id)
    result = await db.execute(stmt)
    profile = result.scalars().first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found."
        )

    update_data = profile_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)

    avatar_url = await s3_client.get_file_url(profile.avatar)

    return ProfileResponseSchema(
        id=profile.id,
        user_id=profile.user_id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        gender=profile.gender,
        date_of_birth=profile.date_of_birth,
        info=profile.info,
        avatar=cast(HttpUrl, avatar_url),
    )
