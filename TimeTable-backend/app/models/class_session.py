from app.extension import db

class ClassSession(db.Model):
    __tablename__ = 'class_sessions'
    id = db.Column(db.Integer, primary_key=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.id', ondelete='CASCADE'), nullable=False)
    semian_id = db.Column(db.Integer, db.ForeignKey('semiani.id', ondelete='CASCADE'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    class_type = db.Column(db.String, nullable=False)

    discipline = db.relationship('Discipline', back_populates='classes', passive_deletes=True, overlaps='classes')
    teacher = db.relationship('Teacher', passive_deletes=True)
    room = db.relationship('Room', passive_deletes=True)
    time_slot = db.relationship('TimeSlot', passive_deletes=True)
    semian = db.relationship('Semian', passive_deletes=True)
    group = db.relationship('Group', passive_deletes=True)