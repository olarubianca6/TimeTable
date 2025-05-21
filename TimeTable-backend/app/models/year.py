from app.extension import db

class Year(db.Model):
    __tablename__ = 'years'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    semiani = db.relationship('Semian', back_populates='year', cascade='all, delete-orphan', passive_deletes=True)
    groups = db.relationship('Group', backref='year', cascade='all, delete-orphan', passive_deletes=True)
    disciplines = db.relationship('Discipline', back_populates='year', cascade='all, delete-orphan', passive_deletes=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name}