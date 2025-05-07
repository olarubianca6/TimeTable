from app.extension import db

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    discipline_links = db.relationship('DisciplineTeacher', back_populates='teacher')
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name}   
