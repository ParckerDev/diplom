from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from models import Equipment
from schemas.equipment import EquipmentBase, EquipmentCreate, Equipment_id


async def create_equipment(
    new_equipment: EquipmentCreate, session: AsyncSession
) -> Equipment:
    """
    Создает новое оборудование в базе данных.

    Аргументы:
        new_equipment (EquipmentCreate): Данные для создания нового оборудования.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        Equipment: Созданный объект оборудования.
    """
    equipment = Equipment(**new_equipment.model_dump())  # Создаем экземпляр Equipment
    session.add(equipment)  # Добавляем оборудование в сессию
    await session.commit()  # Коммитим изменения в базе данных
    await session.refresh(equipment)  # Обновляем объект оборудования
    return equipment  # Возвращаем созданное оборудование


async def get_all_equipment(session: AsyncSession) -> list[Equipment_id]:
    """
    Получает список всего оборудования из базы данных.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        list[Equipment_id]: Список объектов оборудования.
    """
    stmt = select(Equipment).order_by(Equipment.id)  # Формируем запрос для получения оборудования
    equipment_list = await session.scalars(stmt)  # Выполняем запрос
    return equipment_list.all()  # Возвращаем все найденные объекты


async def get_equipment_by_id(session: AsyncSession, equipment_id: int) -> Equipment:
    """
    Получает оборудование по его идентификатору.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        equipment_id (int): Идентификатор оборудования.

    Возвращает:
        Equipment: Объект оборудования с указанным идентификатором.
    """
    stmt = select(Equipment).where(Equipment.id == equipment_id)  # Формируем запрос для получения оборудования по ID
    equipment = await session.scalar(stmt)  # Выполняем запрос
    return equipment  # Возвращаем найденное оборудование


async def update_equipment(
    equipment_id: int, equipment_data: EquipmentBase, session: AsyncSession
) -> Equipment:
    """
    Обновляет данные оборудования в базе данных.

    Аргументы:
        equipment_id (int): Идентификатор оборудования для обновления.
        equipment_data (EquipmentBase): Новые данные для обновления оборудования.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        Equipment: Обновленный объект оборудования.
    """
    stmt = (
        update(Equipment)
        .where(Equipment.id == equipment_id)
        .values(**equipment_data.model_dump())  # Обновляем значения оборудования
        .execution_options(synchronize_session="fetch")  # Синхронизируем сессию
    )
    await session.execute(stmt)  # Выполняем обновление
    await session.commit()  # Коммитим изменения

    # Получаем обновленное оборудование
    updated_equipment = await session.get(Equipment, equipment_id)  # Получаем обновленный объект
    return updated_equipment  # Возвращаем обновленное оборудование


async def delete_equipment(session: AsyncSession, equipment_id: int) -> bool:
    """
    Удаляет оборудование из базы данных по его идентификатору.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        equipment_id (int): Идентификатор оборудования для удаления.

    Возвращает:
        bool: True, если оборудование было успешно удалено, иначе False.
    """
    stmt = delete(Equipment).where(Equipment.id == equipment_id)  # Формируем запрос на удаление
    result = await session.execute(stmt)  # Выполняем удаление
    await session.commit()  # Коммитим изменения
    return result.rowcount > 0  # Возвращаем True, если удалено хотя бы одно оборудование
