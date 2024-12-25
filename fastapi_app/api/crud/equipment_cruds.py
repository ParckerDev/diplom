from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from models import Equipment
from schemas.equipment import EquipmentBase, EquipmentCreate, Equipment_id


async def create_equipment(
    new_equipment: EquipmentCreate, session: AsyncSession
) -> Equipment:
    equipment = Equipment(**new_equipment.model_dump())
    session.add(equipment)
    await session.commit()
    await session.refresh(equipment)
    return equipment


async def get_all_equipment(session: AsyncSession) -> list[Equipment_id]:
    stmt = select(Equipment).order_by(Equipment.id)
    equipment_list = await session.scalars(stmt)
    return equipment_list.all()


async def get_equipment_by_id(session: AsyncSession, equipment_id: int) -> Equipment:
    stmt = select(Equipment).where(Equipment.id == equipment_id)
    equipment = await session.scalar(stmt)
    return equipment


async def update_equipment(
    equipment_id: int, equipment_data: EquipmentBase, session: AsyncSession
) -> Equipment:
    stmt = (
        update(Equipment)
        .where(Equipment.id == equipment_id)
        .values(**equipment_data.model_dump())
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(stmt)
    await session.commit()

    # Получаем обновленное оборудование
    updated_equipment = await session.get(Equipment, equipment_id)
    return updated_equipment


async def delete_equipment(session: AsyncSession, equipment_id: int) -> bool:
    stmt = delete(Equipment).where(Equipment.id == equipment_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
