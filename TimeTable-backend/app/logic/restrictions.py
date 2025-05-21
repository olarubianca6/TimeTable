from datetime import time

def valid_class_time(day, hour):
    if not isinstance(hour, time):
        return False
    else:
        return (
        day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] and
        (
            hour.hour > 8 or (hour.hour == 8 and hour.minute >= 0)
        ) and
        (
            hour.hour < 20 or (hour.hour == 20 and hour.minute == 0)
        )
    )

def match_room_class_type(room_type, class_type):
    room_type = room_type.lower()
    class_type = class_type.lower()
    if class_type == "course":
        return room_type == "course"
    elif class_type == "laboratory":
        return room_type in ["laboratory", "seminar/laboratory"]
    elif class_type == "seminar":
        return room_type in ["course", "laboratory", "seminar", "seminar/laboratory"]
    return False