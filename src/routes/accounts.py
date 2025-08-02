from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from src.database.session_postgresql import get_postgresql_db
from src.config.dependencies import (
    get_jwt_auth_manager,
    get_settings,
    BaseAppSettings,
    get_accounts_email_notificator
)
from src.database.models.accounts import (
    UserModel,
    UserGroupModel,
    UserGroupEnum,
    ActivationTokenModel,
)
from src.schemas.accounts import (
    UserRegistrationRequestSchema,
    UserRegistrationResponseSchema,
)
from src.notifications.interfaces import EmailSenderInterface

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRegistrationResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="User Registration",
    description="Register a new user with an email and password.",
    responses={
        409: {"description": "User with this email already exists."},
        500: {"description": "An error occurred during user creation."},
    },
)
async def register_user(
    user_data: UserRegistrationRequestSchema,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_postgresql_db),
    email_sender: EmailSenderInterface = Depends(get_accounts_email_notificator),
) -> UserRegistrationResponseSchema:
    existing_user_result = await db.execute(
        select(UserModel).where(UserModel.email == user_data.email)
    )
    if existing_user_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with this email {user_data.email} already exists.",
        )

    user_group_result = await db.execute(
        select(UserGroupModel).where(UserGroupModel.name == UserGroupEnum.USER)
    )
    user_group = user_group_result.scalar_one_or_none()
    if not user_group:
        user_group = UserGroupModel(name=UserGroupEnum.USER)
        db.add(user_group)
        await db.flush()

    try:
        new_user = UserModel.create(
            email=str(user_data.email),
            raw_password=user_data.password,
            group_id=user_group.id,
        )
        db.add(new_user)
        await db.flush()

        activation_token = ActivationTokenModel(user_id=new_user.id)
        db.add(activation_token)

        await db.commit()
        await db.refresh(new_user)
        await db.refresh(activation_token)

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during user creation.",
        ) from e

    activation_link = (
        f"http://localhost:8000/api/v1/accounts/activate?token={activation_token.token}"
    )
    background_tasks.add_task(
        email_sender.send_activation_email, new_user.email, activation_link
    )

    return UserRegistrationResponseSchema.model_validate(new_user)
