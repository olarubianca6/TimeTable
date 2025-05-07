from app.extension import db


class Year(db.Model):
    __tablename__ = 'years'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    groups = db.relationship('Group', backref='years', cascade='all, delete-orphan')
    disciplines = db.relationship('Discipline', back_populates='year', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name}