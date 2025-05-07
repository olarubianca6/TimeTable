from app.extension import db

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('years.id'), nullable=False)
    semian = db.Column(db.String, nullable=False)

    disciplines = db.relationship('Discipline', back_populates='group', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'year_id': self.year_id}