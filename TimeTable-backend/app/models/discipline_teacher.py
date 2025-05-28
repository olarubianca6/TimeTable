from app.extension import db

class DisciplineTeacher(db.Model):
    __tablename__ = 'discipline_teacher'
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='CASCADE'), primary_key=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id', ondelete='CASCADE'), primary_key=True)

    teacher = db.relationship('Teacher', back_populates='discipline_links', passive_deletes=True)
    discipline = db.relationship('Discipline', back_populates='teacher_links', passive_deletes=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert self.teacher_id is not None
        assert self.discipline_id is not None