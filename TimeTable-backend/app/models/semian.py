from app.extension import db

class Semian(db.Model):
    __tablename__ = 'semiani'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('years.id', ondelete='CASCADE'), nullable=False)

    year = db.relationship('Year', back_populates='semian', passive_deletes=True)
    groups = db.relationship('Group', back_populates='semian', cascade='all, delete-orphan', passive_deletes=True)