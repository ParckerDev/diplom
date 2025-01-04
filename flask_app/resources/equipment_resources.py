from flask_restful import Resource, reqparse
from schemas.equipment_schema import EquipmentCreate, EquipmentResponse
from cruds.equipment_crud import create_equipment, get_equipment, get_all_equipment

equipment_parser = reqparse.RequestParser()
equipment_parser.add_argument('name', required=True, help='Name cannot be blank')
equipment_parser.add_argument('description')
equipment_parser.add_argument('cost', type=int, required=True, help='Cost cannot be blank')

class EquipmentResource(Resource):
    def post(self):
        args = equipment_parser.parse_args()
        equipment_data = EquipmentCreate(**args)
        new_equipment = create_equipment(equipment_data)
        return EquipmentResponse.model_validate(new_equipment), 201

    def get(self, equipment_id):
        equipment = get_equipment(equipment_id)
        if equipment:
            return EquipmentResponse.model_validate(equipment), 200
        return {'message': 'Equipment not found'}, 404

class EquipmentListResource(Resource):
    def get(self):
        equipment = get_all_equipment()
        return [EquipmentResponse.model_validate(equip) for equip in equipment], 200
