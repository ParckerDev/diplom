from app import db

class Equipment(db.Model):
    __tablename__ = 'equipments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Equipment {self.name}>'
