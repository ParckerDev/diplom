from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.db_help import db_helper
from schemas.equipment import EquipmentBase, EquipmentCreate
from .crud.equipment_cruds import (
    create_equipment,
    delete_equipment,
    get_all_equipment,
    get_equipment_by_id,
    update_equipment,
)

router = APIRouter(prefix="/equipment", tags=["Equipment"])
conn = Annotated[AsyncSession, Depends(db_helper.get_session)]


@router.get("", response_model=list[EquipmentBase])
async def get_equipments(session=conn):
    equipments = await get_all_equipment(session=session)
    return equipments


@router.post("", response_model=EquipmentBase)
async def create_equipment_endpoint(new_equipment: EquipmentCreate, session: conn):
    equipment = await create_equipment(new_equipment=new_equipment, session=session)
    return equipment


@router.get("/{equipment_id}", response_model=EquipmentBase)
async def get_equipment_by_id_endpoint(equipment_id: int, session: conn):
    equipment = await get_equipment_by_id(session=session, equipment_id=equipment_id)
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.put("/{equipment_id}", response_model=EquipmentBase)
async def update_equipment_endpoint(
    equipment_id: int, equipment_data: EquipmentBase, session: conn
):
    updated_equipment = await update_equipment(
        equipment_id=equipment_id, equipment_data=equipment_data, session=session
    )
    if updated_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return updated_equipment


@router.delete("/{equipment_id}", response_model=dict)
async def delete_equipment_endpoint(equipment_id: int, session: conn):
    deleted = await delete_equipment(session=session, equipment_id=equipment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return {"detail": "Equipment deleted successfully"}
