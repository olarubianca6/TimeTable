from app import db

class DisciplineTeacher(db.Model):
    __tablename__ = 'discipline_teacher'
    id = db.Column(db.Integer, primary_key=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)

    course_hours = db.Column(db.Integer, default=0)
    seminar_hours = db.Column(db.Integer, default=0)
    lab_hours = db.Column(db.Integer, default=0)

    discipline = db.relationship('Discipline', back_populates='teacher_links')
    teacher = db.relationship('Teacher', back_populates='disciplines')