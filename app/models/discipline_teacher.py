from app import db

class DisciplineTeacher(db.Model):
    __tablename__ = 'discipline_teacher'
    id = db.Column(db.Integer, primary_key=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)

    discipline = db.relationship('Discipline', back_populates='teacher_links')
    teacher = db.relationship('Teacher', back_populates='disciplines')