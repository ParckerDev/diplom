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
    rental = await session.scalar(stmt)
    return rental


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


async def update_rental(session: AsyncSession, rental_id: int, rental_data: RentalBase):
    updated_rental = await get_rental_by_id(session=session, rental_id=rental_id)
    if updated_rental:
        stmt = update(Rental).where(Rental.id==rental_id).values(**rental_data.model_dump())
        await session.execute(stmt)
        await session.commit()
        updated_rental = await session.get(Rental, rental_id)
        return updated_rental
    return None

async def delete_rental(session: AsyncSession, rental_id: int):
    deleted_rental = get_rental_by_id(session=session, rental_id=rental_id)
    if deleted_rental is not None:
        stmt = delete(Rental).where(Rental.id==rental_id)
        result = await session.execute(stmt)
        await session.commit()
        return result
    return None