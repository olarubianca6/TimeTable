from datetime import time

def valid_class_time(day, hour):
    if isinstance(hour, time):
        hour_int = hour.hour
    else:
        print("Eroare: `hour` nu este un obiect de tip datetime.time")
        return False

    return day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] and 8 <= hour_int <= 20


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