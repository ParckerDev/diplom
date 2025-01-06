from flask_restful import Resource, reqparse
from schemas.rental_schema import RentalCreate, RentalResponse
from cruds.rental_crud import create_rental, get_rental, get_all_rentals

rental_parser = reqparse.RequestParser()
rental_parser.add_argument('equipment_id', type=int, required=True, help='Equipment ID cannot be blank')
rental_parser.add_argument('user_id', type=int, required=True, help='User ID cannot be blank')
rental_parser.add_argument('start_date', required=True, help='Start date cannot be blank')
rental_parser.add_argument('end_date', required=True, help='End date cannot be blank')

class RentalResource(Resource):
    def post(self):
        args = rental_parser.parse_args()
        rental_data = RentalCreate(**args)
        new_rental = create_rental(rental_data)
        return RentalResponse.model_validate(new_rental), 201

    def get(self, rental_id):
        rental = get_rental(rental_id)
        if rental:
            return RentalResponse.model_validate(rental), 200
        return {'message': 'Rental not found'}, 404

class RentalListResource(Resource):
    def get(self):
        rentals = get_all_rentals()
        return [RentalResponse.model_validate(rent) for rent in rentals], 200
