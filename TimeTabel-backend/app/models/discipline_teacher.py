from app.extension import db

class DisciplineTeacher(db.Model):
    __tablename__ = 'discipline_teacher'

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), primary_key=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'), primary_key=True)

    teacher = db.relationship('Teacher', back_populates='discipline_links')
    discipline = db.relationship('Discipline', back_populates='teacher_links')
