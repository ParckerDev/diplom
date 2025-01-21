from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from models import Rental
from schemas.rental import RentalBase, RentalCreate, Rental_id
from .equipment_cruds import get_equipment_by_id


async def get_all_rental(session: AsyncSession):
    """
    Получает список всех аренды из базы данных.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        list: Список всех объектов аренды.
    """
    stmt = select(Rental).order_by(Rental.id)  # Формируем запрос для получения всех аренды
    rental_list = await session.scalars(stmt)  # Выполняем запрос
    return rental_list.all()  # Возвращаем все найденные объекты


async def get_rental_by_equipment(session: AsyncSession, equipment_id: int):
    """
    Получает список аренды по идентификатору оборудования.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        equipment_id (int): Идентификатор оборудования.

    Возвращает:
        list: Список объектов аренды для указанного оборудования.
    """
    stmt = select(Rental).filter(Rental.equipment_id == equipment_id)  # Формируем запрос для получения аренды по ID оборудования
    rental_list = await session.scalars(stmt)  # Выполняем запрос
    return rental_list.all()  # Возвращаем все найденные объекты


async def get_rental_by_id(session: AsyncSession, rental_id: int):
    """
    Получает аренду по ее идентификатору.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        rental_id (int): Идентификатор аренды.

    Возвращает:
        Rental: Объект аренды с указанным идентификатором или None, если не найдено.
    """
    stmt = select(Rental).filter(Rental.id == rental_id)  # Формируем запрос для получения аренды по ID
    rental = await session.scalar(stmt)  # Выполняем запрос
    return rental  # Возвращаем найденную аренду или None


async def create_rental(session: AsyncSession, new_rental: RentalCreate):
    """
    Создает новую аренду в базе данных.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        new_rental (RentalCreate): Данные для создания новой аренды.

    Возвращает:
        Rental: Созданный объект аренды или None, если аренда не может быть создана.
    """
    new_rent = Rental(**new_rental.model_dump())  # Создаем экземпляр Rental

    # Проверяем, есть ли пересечения с существующими арендами
    stmt = select(Rental).filter(
        Rental.equipment_id == new_rent.equipment_id,
        Rental.start_date < new_rent.end_date,
        Rental.end_date > new_rent.start_date,
    )

    rental_list = await session.execute(stmt)
    existing_rentals = rental_list.scalars().all()  # Получаем все существующие аренды

    if existing_rentals:  # Если есть существующие аренды, возвращаем None
        return None
    else:
        session.add(new_rent)  # Добавляем новую аренду в сессию
        await session.commit()  # Коммитим изменения
        await session.refresh(new_rent)  # Обновляем объект аренды
        return new_rent  # Возвращаем созданную аренду


async def update_rental(session: AsyncSession, rental_id: int, rental_data: RentalBase):
    """
    Обновляет данные аренды в базе данных.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        rental_id (int): Идентификатор аренды для обновления.
        rental_data (RentalBase): Новые данные для обновления аренды.

    Возвращает:
        Rental: Обновленный объект аренды или сообщение об ошибке.
    """
    updated_rental = await get_rental_by_id(session=session, rental_id=rental_id)
    if updated_rental:
        stmt = (
            update(Rental)
            .where(Rental.id == rental_id)
            .values(**rental_data.model_dump())  # Обновляем значения аренды
        )
        await session.execute(stmt)  # Выполняем обновление
        await session.commit()  # Коммитим изменения
       
