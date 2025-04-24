from app import db

class Year(db.Model):
    __tablename__ = 'years'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    groups = db.relationship('Group', backref='year', cascade='all, delete-orphan')
    disciplines = db.relationship('Discipline', backref='year', cascade='all, delete-orphan')