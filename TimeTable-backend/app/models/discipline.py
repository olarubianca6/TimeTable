from app.extension import db

class Discipline(db.Model):
    __tablename__ = 'disciplines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('years.id', ondelete='CASCADE'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=True)

    teacher_links = db.relationship('DisciplineTeacher', back_populates='discipline', cascade='all, delete-orphan')
    classes = db.relationship('ClassSession', back_populates='discipline', cascade='all, delete-orphan')

    year = db.relationship('Year', back_populates='disciplines', passive_deletes=True)
    group = db.relationship('Group', back_populates='disciplines', passive_deletes=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert self.name
        assert self.year_id is not None

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'year_id': self.year_id, 'group_id': self.group_id}