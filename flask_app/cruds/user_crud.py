from app import db
from models.user_model import User
from schemas.user_schema import UserCreate

def create_user(user_data: UserCreate) -> User:
    new_user = User(name=user_data.name, email=user_data.email)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user(user_id: int) -> User:
    return User.query.get(user_id)

def get_all_users() -> list[User]:
    return User.query.all()
