from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.db_help import db_helper
from schemas.rental import Rental_id, RentalBase, RentalCreate
from .crud.rental_cruds import create_rental, get_all_rental, get_rental_by_equipment, get_rental_by_id


router = APIRouter(prefix="/rental", tags=["RENTAL"])
conn = Annotated[AsyncSession, Depends(db_helper.get_session)]


@router.post('', response_model=Rental_id)
async def rental_create(session: conn, new_rent: RentalCreate):
    rental = await create_rental(session=session, new_rental=new_rent)
    return rental