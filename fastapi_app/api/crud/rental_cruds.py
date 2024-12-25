from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from models import Rental
from schemas.rental import RentalBase, RentalCreate, Rental_id


async def get_all_rental(session: AsyncSession):
    stmt = select(Rental).order_by(Rental.id)
    rental_list = await session.scalars(stmt)
    return rental_list.all()


async def get_rental_by_equipment(session: AsyncSession, equipment_id: int):
    stmt = select(Rental).filter(Rental.equipment_id == equipment_id)
    rental_list = await session.scalars(stmt)
    return rental_list.all()


async def get_rental_by_id(session: AsyncSession, rental_id: int):
    stmt = select(Rental).filter(Rental.id == rental_id)
    rental_list = await session.scalars(stmt)
    return rental_list.all()


async def create_rental(session: AsyncSession, new_rental: RentalCreate):
    new_rent = RentalCreate(**new_rental.model_dump())
    stmt = select(Rental).filter(
        Rental.equipment_id == new_rent.equipment_id,
        Rental.start_date <= new_rent.end_date,
        Rental.end_date >= new_rent.start_date,
    )
    rental_list = await session.scalars(stmt)
    if rental_list.all():
        return Response({"error": "Оборудование занято на эти даты"})
    session.add(new_rent)
    await session.commit()
    await session.refresh(new_rent)
    return new_rent


#async def update_rental()