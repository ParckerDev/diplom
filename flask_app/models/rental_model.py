from app import db

class Rental(db.Model):
    __tablename__ = 'rentals'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    equipment = db.relationship('Equipment', backref='rentals')
    user = db.relationship('User', backref='rentals')

    def __repr__(self):
        return f'<Rental {self.id}>'
