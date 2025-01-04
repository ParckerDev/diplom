from app import db
from models.equipment_model import Equipment
from schemas.equipment_schema import EquipmentCreate

def create_equipment(equipment_data: EquipmentCreate) -> Equipment:
    new_equipment = Equipment(
        name=equipment_data.name,
        description=equipment_data.description,
        cost=equipment_data.cost
    )
    db.session.add(new_equipment)
    db.session.commit()
    return new_equipment

def get_equipment(equipment_id: int) -> Equipment:
    return Equipment.query.get(equipment_id)

def get_all_equipment() -> list[Equipment]:
    return Equipment.query.all()
