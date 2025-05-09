from app.extension import db

class TimeSlot(db.Model):
    __tablename__ = 'time_slots'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)