from app.extension import db

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('years.id', ondelete='CASCADE'), nullable=False)
    semian_id = db.Column(db.Integer, db.ForeignKey('semiani.id', ondelete='CASCADE'), nullable=False)

    semian = db.relationship('Semian', back_populates='groups', passive_deletes=True)
    disciplines = db.relationship('Discipline', back_populates='group', cascade='all, delete-orphan', passive_deletes=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'year': {
                'id': self.year.id,
                'name': self.year.name
            } if self.year else None,
            'semian': {
                'id': self.semian.id,
                'name': self.semian.name
            } if self.semian else None
        }

