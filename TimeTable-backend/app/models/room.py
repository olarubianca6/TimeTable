from app.extension import db

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    room_type = db.Column(db.String(20), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert self.name
        assert self.room_type in ["course", "laboratory", "seminar", "seminar/laboratory"]


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'room_type': self.room_type
        }