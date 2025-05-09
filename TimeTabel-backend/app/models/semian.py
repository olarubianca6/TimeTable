from app.extension import db

class Semian(db.Model):
    __tablename__ = 'semiani'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('years.id'), nullable=False)

    year = db.relationship('Year', back_populates='semiani')
    groups = db.relationship('Group', back_populates='semiani', cascade='all, delete-orphan')