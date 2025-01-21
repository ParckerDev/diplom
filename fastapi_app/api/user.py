from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.db_help import db_helper
from schemas.user import UserCreate, UserBase, User_id
from .crud.usercruds import (
    create_user,
    get_users,
    delete_user,
    get_user_by_id,
    user_update,
)

router = APIRouter(prefix="/user", tags=["USER"])
conn = Annotated[AsyncSession, Depends(db_helper.get_session)]


@router.post("", response_model=User_id)
async def user_create(new_user: UserCreate, session: conn):
    """
    Создает нового пользователя.

    Аргументы:
        new_user (UserCreate): Данные нового пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        User_id: Созданный пользователь с его идентификатором.
    """
    user = await create_user(new_user, session)
    return user


@router.get("", response_model=list[User_id])
async def get_all_users(session: conn):
    """
    Получает список всех пользователей.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        list[User_id]: Список пользователей.
    """
    users = await get_users(session=session)
    return users


@router.get("/{user_id}", response_model=User_id)
async def get_user_id(session: conn, user_id: int):
    """
    Получает пользователя по его идентификатору.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        user_id (int): Идентификатор пользователя.

    Возвращает:
        User_id: Данные пользователя.

    Исключения:
        HTTPException: Если пользователь не найден, возвращает 404.
    """
    user = await get_user_by_id(session=session, user_id=user_id)
    return user


@router.delete("/{user_id}", response_model=dict)
async def del_user(session: conn, user_id: int):
    """
    Удаляет пользователя по его идентификатору.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        user_id (int): Идентификатор пользователя для удаления.

    Возвращает:
        dict: Сообщение об успешном удалении.

    Исключения:
        HTTPException: Если пользователь не найден, возвращает 404.
    """
    deleted = await delete_user(session=session, user_id=user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found!")
    return {"detail": "User deleted successfully"}


@router.put("/{user_id}", response_model=User_id)
async def update_user(session: conn, user_id: int, user_data: UserBase):
    """
    Обновляет данные пользователя по его идентификатору.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        user_id (int): Идентификатор пользователя для обновления.
        user_data (UserBase): Новые данные пользователя.

    Возвращает:
        User_id: Обновленные данные пользователя.

    Исключения:
        HTTPException: Если пользователь не найден, возвращает 404.
    """
    updated_user = await user_update(
        session=session, user_id=user_id, user_data=user_data
    )
    if updated_user:
        return updated_user
    raise HTTPException(status_code=404, detail="User not found!")
