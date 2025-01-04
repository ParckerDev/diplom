from app import db
from models.rental_model import Rental
from schemas.rental_schema import RentalCreate

def create_rental(rental_data: RentalCreate) -> Rental:
    new_rental = Rental(
        equipment_id=rental_data.equipment_id,
        user_id=rental_data.user_id,
        start_date=rental_data.start_date,
        end_date=rental_data.end_date
    )
    db.session.add(new_rental)
    db.session.commit()
    return new_rental

def get_rental(rental_id: int) -> Rental:
    return Rental.query.get(rental_id)

def get_all_rentals() -> list[Rental]:
    return Rental.query.all()
