from app.extension import db

class ClassSession(db.Model):
    __tablename__ = 'class_sessions'
    id = db.Column(db.Integer, primary_key=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.id'), nullable=False)
    semian_id = db.Column(db.Integer, db.ForeignKey('semiani.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    class_type = db.Column(db.String, nullable=False)

    discipline = db.relationship('Discipline', passive_deletes=True)
    teacher = db.relationship('Teacher', passive_deletes=True)

    room = db.relationship('Room')
    time_slot = db.relationship('TimeSlot')
    semian = db.relationship('Semian')
    group = db.relationship('Group')