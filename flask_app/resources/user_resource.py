from flask_restful import Resource, reqparse
from schemas.user_schema import UserCreate, UserResponse
from cruds.user_crud import create_user, get_user, get_all_users

user_parser = reqparse.RequestParser()
user_parser.add_argument('name', required=True, help='Name cannot be blank')
user_parser.add_argument('email', required=True, help='Email cannot be blank')

class UserResource(Resource):
    def post(self):
        args = user_parser.parse_args()
        user_data = UserCreate(**args)
        new_user = create_user(user_data)
        return UserResponse.model_validate(new_user), 201

    def get(self, user_id):
        user = get_user(user_id)
        if user:
            return UserResponse.model_validate(user), 200
        return {'message': 'User not found'}, 404

class UserListResource(Resource):
    def get(self):
        users = get_all_users()
        return [UserResponse.model_validate(user) for user in users], 200
