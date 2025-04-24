from app import db

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('years.id'), nullable=False)

    students = db.relationship('Student', backref='group', cascade='all, delete-orphan')
    disciplines = db.relationship('Discipline', backref='group', cascade='all, delete-orphan')