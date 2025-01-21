from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.db_help import db_helper
from schemas.rental import Rental_id, RentalBase, RentalCreate
from .crud.rental_cruds import (
    create_rental,
    get_all_rental,
    get_rental_by_equipment,
    get_rental_by_id,
    delete_rental,
    update_rental,
)

# Создаем маршрутизатор для управления арендой
router = APIRouter(prefix="/rental", tags=["RENTAL"])
conn = Annotated[AsyncSession, Depends(db_helper.get_session)]  # Зависимость для получения сессии базы данных


@router.post("", response_model=Rental_id)
async def rental_create(session: conn, new_rent: RentalCreate):
    """
    Создает новую аренду.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        new_rent (RentalCreate): Данные для создания новой аренды.

    Возвращает:
        Rental_id: Созданный объект аренды.

    Исключения:
        HTTPException: Если оборудование занято или не найдено оборудование с указанным ID, возвращает 400.
    """
    rental = await create_rental(session=session, new_rental=new_rent)  # Создаем новую аренду
    if not rental:
        raise HTTPException(
            status_code=400,
            detail="Оборудование занято на эти даты или нет оборудования с таким id!",
        )  # Возвращаем ошибку, если аренда не может быть создана
    return rental  # Возвращаем созданную аренду


@router.get("", response_model=list[Rental_id])
async def get_rentals(session: conn):
    """
    Получает список всех аренд.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Возвращает:
        list[Rental_id]: Список объектов аренды.
    """
    rentals = await get_all_rental(session=session)  # Получаем все аренды
    return rentals  # Возвращаем список аренд


@router.get("/{rent_id}", response_model=Rental_id)
async def get_rent_id(session: conn, rent_id: int):
    """
    Получает аренду по ее идентификатору.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        rent_id (int): Идентификатор аренды.

    Возвращает:
        Rental_id: Объект аренды с указанным идентификатором.

    Исключения:
        HTTPException: Если аренда не найдена, возвращает 404.
    """
    rental = await get_rental_by_id(session=session, rental_id=rent_id)  # Получаем аренду по ID
    if not rental:
        raise HTTPException(
            status_code=404, detail=f"Аренда с id={rent_id} не найдена!"
        )  # Возвращаем ошибку, если не найдено
    return rental  # Возвращаем найденную аренду


@router.get("/eq/{equipment_id}", response_model=list[Rental_id])
async def get_rent_eq(session: conn, equipment_id: int):
    """
    Получает список аренд по идентификатору оборудования.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        equipment_id (int): Идентификатор оборудования.

    Возвращает:
        list[Rental_id]: Список объектов аренды для указанного оборудования.
    """
    rental_list = await get_rental_by_equipment(
        session=session, equipment_id=equipment_id
    )  # Получаем аренды по ID оборудования
    return rental_list  # Возвращаем список аренд


@router.delete("/{rent_id}", response_model=dict)
async def delete_rent(session: conn, rent_id: int):
    """
    Удаляет аренду по ее идентификатору.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        rent_id (int): Идентификатор аренды для удаления.

    Возвращает:
        dict: Сообщение об успешном удалении.

    Исключения:
        HTTPException: Если аренда не найдена, возвращает 404.
    """
    deleted = await delete_rental(session=session, rental_id=rent_id)  # Удаляем аренду
    if not deleted:
        raise HTTPException(status_code=404, detail="Аренда не найдена")  # Возвращаем ошибку, если аренда не найдена
    return {"detail": "Rental deleted successfully"}  # Возвращаем сообщение об успешном удалении


@router.put("/{rent_id}")
async def update_rent(session: conn, rent_id: int, rental_data: RentalBase):
    """
    Обновляет данные аренды.

    Аргументы:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        rent_id (int): Идентификатор аренды для обновления.
        rental_data (RentalBase): Новые данные для обновления аренды.

    Возвращает:
        RentalBase: Обновленный объект аренды.

    Исключения:
        HTTPException: Если аренда не найдена, возвращает 404.
    """
    updated_rent = await update_rental(
        session=session, rental_id=rent_id, rental_data=rental_data
    )  # Обновляем аренду
    if updated_rent is None:
        raise HTTPException(status_code=404, detail="Rent not found")  # Возвращаем ошибку, если аренда не найдена
    return updated_rent  # Возвращаем обновленную аренду
