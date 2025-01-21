from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.db_help import db_helper
from schemas.equipment import EquipmentBase, EquipmentCreate, Equipment_id
from .crud.equipment_cruds import (
    create_equipment,
    delete_equipment,
    get_all_equipment,
    get_equipment_by_id,
    update_equipment,
)

# Создаем маршрутизатор для управления оборудованием
router = APIRouter(prefix="/equipment", tags=["EQUIPMENTS"])
conn = Annotated[AsyncSession, Depends(db_helper.get_session)]  # Зависимость для получения сессии базы данных


@router.get("", response_model=list[Equipment_id])
async def get_equipments(session: conn):
    """
    Получает список всего оборудования.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        list[Equipment_id]: Список объектов оборудования.
    """
    equipments = await get_all_equipment(session=session)  # Получаем все оборудование
    return equipments  # Возвращаем список оборудования


@router.post("", response_model=Equipment_id)
async def equipment_create(new_equipment: EquipmentCreate, session: conn):
    """
    Создает новое оборудование.

    Аргументы:
        new_equipment (EquipmentCreate): Данные для создания нового оборудования.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        Equipment_id: Созданный объект оборудования.
    """
    equipment = await create_equipment(new_equipment=new_equipment, session=session)  # Создаем новое оборудование
    return equipment  # Возвращаем созданное оборудование


@router.get("/{equipment_id}", response_model=EquipmentBase)
async def get_equipment_by_id_endpoint(equipment_id: int, session: conn):
    """
    Получает оборудование по его идентификатору.

    Аргументы:
        equipment_id (int): Идентификатор оборудования.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        EquipmentBase: Объект оборудования с указанным идентификатором.

    Исключения:
        HTTPException: Если оборудование не найдено, возвращает 404.
    """
    equipment = await get_equipment_by_id(session=session, equipment_id=equipment_id)  # Получаем оборудование по ID
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")  # Возвращаем ошибку, если не найдено
    return equipment  # Возвращаем найденное оборудование


@router.put("/{equipment_id}", response_model=EquipmentBase)
async def update_equipment_endpoint(
    equipment_id: int, equipment_data: EquipmentBase, session: conn
):
    """
    Обновляет данные оборудования.

    Аргументы:
        equipment_id (int): Идентификатор оборудования для обновления.
        equipment_data (EquipmentBase): Новые данные для обновления оборудования.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        EquipmentBase: Обновленный объект оборудования.

    Исключения:
        HTTPException: Если оборудование не найдено, возвращает 404.
    """
    updated_equipment = await update_equipment(
        equipment_id=equipment_id, equipment_data=equipment_data, session=session
    )  # Обновляем оборудование
    if updated_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")  # Возвращаем ошибку, если не найдено
    return updated_equipment  # Возвращаем обновленное оборудование


@router.delete("/{equipment_id}", response_model=dict)
async def delete_equipment_endpoint(equipment_id: int, session: conn):
    """
    Удаляет оборудование по его идентификатору.

    Аргументы:
        equipment_id (int): Идентификатор оборудования для удаления.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        dict: Сообщение об успешном удалении.

    Исключения:
        HTTPException: Если оборудование не найдено, возвращает 404.
    """
    deleted = await delete_equipment(session=session, equipment_id=equipment_id)  # Удаляем оборудование
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipment not found")  # Возвращаем ошибку, если не найдено
    return {"detail": "Equipment deleted successfully"}  # Возвращаем сообщение об успешном удалении
