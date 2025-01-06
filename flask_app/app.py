from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rentals.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
api = Api(app)
from resources.user_resource import UserResource, UserListResource
from resources.equipment_resources import EquipmentResource, EquipmentListResource
from resources.rental_resource import RentalResource, RentalListResource


api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/users/<int:user_id>")
api.add_resource(EquipmentListResource, "/equipment")
api.add_resource(EquipmentResource, "/equipment/<int:equipment_id>")
api.add_resource(RentalListResource, "/rentals")
api.add_resource(RentalResource, "/rentals/<int:rental_id>")

if __name__ == "__main__":
    app.run(debug=True)
