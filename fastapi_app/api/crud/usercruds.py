from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from models import User
from schemas.user import User_id, UserCreate, UserBase


async def create_user(new_user: UserCreate, session: AsyncSession) -> User:
    """
    Создает нового пользователя в базе данных.

    Аргументы:
        new_user (UserCreate): Данные для создания нового пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        User: Созданный объект пользователя.
    """
    user = User(**new_user.model_dump())  # Создаем экземпляр User
    session.add(user)  # Добавляем пользователя в сессию
    await session.commit()  # Коммитим изменения в базе данных
    await session.refresh(user)  # Обновляем объект пользователя
    return user  # Возвращаем созданного пользователя


async def get_users(session: AsyncSession) -> list[User_id]:
    """
    Получает список всех пользователей из базы данных.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        list[User_id]: Список всех объектов пользователей.
    """
    stmt = select(User).order_by(User.id)  # Формируем запрос для получения всех пользователей
    users = await session.scalars(stmt)  # Выполняем запрос
    return users.all()  # Возвращаем все найденные объекты


async def get_user_by_id(session: AsyncSession, user_id: int):
    """
    Получает пользователя по его идентификатору.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        user_id (int): Идентификатор пользователя.

    Возвращает:
        User: Объект пользователя с указанным идентификатором или None, если не найдено.
    """
    stmt = select(User).where(User.id == user_id)  # Формируем запрос для получения пользователя по ID
    user = await session.scalar(stmt)  # Выполняем запрос
    return user  # Возвращаем найденного пользователя или None


async def delete_user(session: AsyncSession, user_id: int):
    """
    Удаляет пользователя из базы данных по его идентификатору.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        user_id (int): Идентификатор пользователя для удаления.

    Возвращает:
        result: Результат выполнения операции удаления или None, если пользователь не найден.
    """
    user = await get_user_by_id(session=session, user_id=user_id)  # Получаем пользователя по ID
    if user is not None:
        stmt = delete(User).where(User.id == user_id)  # Формируем запрос на удаление
        result = await session.execute(stmt)  # Выполняем удаление
        await session.commit()  # Коммитим изменения
        return result  # Возвращаем результат удаления
    return None  # Возвращаем None, если пользователь не найден


async def user_update(session: AsyncSession, user_id: int, user_data: UserBase):
    """
    Обновляет данные пользователя в базе данных.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        user_id (int): Идентификатор пользователя для обновления.
        user_data (UserBase): Новые данные для обновления пользователя.

    Возвращает:
        User: Обновленный объект пользователя или None, если пользователь не найден.
    """
    updated_user = await get_user_by_id(session=session, user_id=user_id)  # Получаем пользователя по ID
    if updated_user:
        stmt = update(User).where(User.id == user_id).values(**user_data.model_dump())  # Формируем запрос на обновление
        await session.execute(stmt)  # Выполняем обновление
        await session.commit()  # Коммитим изменения
        update_user = await session.get(User, user_id)  # Получаем обновленный объект
        return update_user  # Возвращаем обновленного пользователя
    return None  # Возвращаем None, если пользователь не найден
