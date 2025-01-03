from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from models import User
from schemas.user import User_id, UserCreate, UserBase


async def create_user(new_user: UserCreate, session: AsyncSession) -> User:
    user = User(**new_user.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_users(session: AsyncSession) -> list[User_id]:
    stmt = select(User).order_by(User.id)
    users = await session.scalars(stmt)
    return users.all()


async def get_user_by_id(session: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    user = await session.scalar(stmt)
    return user


async def delete_user(session: AsyncSession, user_id: int):
    user = await get_user_by_id(session=session, user_id=user_id)
    if user is not None:
        stmt = delete(User).where(User.id == user_id)
        result = await session.execute(stmt)
        await session.commit()
        return result
    return None


async def user_update(session: AsyncSession, user_id: int, user_data: UserBase):
    updated_user = get_user_by_id(session=session, user_id=user_id)
    if updated_user:
        stmt = update(User).where(User.id == user_id).values(**user_data.model_dump())
        await session.execute(stmt)
        await session.commit()
        update_user = await session.get(User, user_id)
        return update_user
    return None