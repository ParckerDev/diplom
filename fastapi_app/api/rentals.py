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
)


router = APIRouter(prefix="/rental", tags=["RENTAL"])
conn = Annotated[AsyncSession, Depends(db_helper.get_session)]


@router.post("", response_model=Rental_id)
async def rental_create(session: conn, new_rent: RentalCreate):
    rental = await create_rental(session=session, new_rental=new_rent)
    return rental


@router.get("", response_model=list[Rental_id])
async def get_rentals(session: conn):
    rentals = await get_all_rental(session=session)
    return rentals


@router.get("/{rental_id}", response_model=Rental_id)
async def get_rent_id(session: conn, rent_id: int):
    rental = await get_rental_by_id(session=session, rental_id=rent_id)
    return rental


@router.get("/{rental_equipment}", response_model=list[Rental_id])
async def get_rent_eq(session: conn, equipment_id: int):
    rental_list = await get_rental_by_equipment(
        session=session, equipment_id=equipment_id
    )
    return rental_list


@router.delete("/{rent_id}", response_model=dict)
async def delete_rent(session: conn, rent_id: int):
    deleted = await delete_rental(session=session, rental_id=rent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Rent not found!")
    return {"detail": "Rental deleted successfully"}
