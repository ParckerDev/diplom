from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rentals.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
api = Api(app)

if __name__ == "__main__":
    app.run(debug=True)
