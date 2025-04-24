from app import db

class Discipline(db.Model):
    __tablename__ = 'disciplines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('years.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)

    teacher_links = db.relationship('DisciplineTeacher', back_populates='discipline')
    classes = db.relationship('ClassSession', backref='discipline', cascade='all, delete-orphan')

    year = db.relationship('Year', backref='disciplines')
    group = db.relationship('Group', backref='disciplines')