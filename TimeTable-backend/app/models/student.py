from app.extension import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert self.name

    def to_dict(self):
        return {'id': self.id, 'name': self.name}