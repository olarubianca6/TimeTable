from app.extension import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    group = db.relationship('Group', back_populates='students')
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'group_id': self.group_id}