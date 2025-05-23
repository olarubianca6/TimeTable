from datetime import time


def valid_class_time(day, hour):
    assert isinstance(day, str), "day must be string"
    assert hour is not None, "hour must not be none"
    if not isinstance(hour, time):
        return False
    return (
            day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] and
            (hour.hour > 8 or (hour.hour == 8 and hour.minute >= 0)) and
            (hour.hour < 20 or (hour.hour == 20 and hour.minute == 0))
    )


def match_room_class_type(room_type, class_type):
    assert isinstance(room_type, str), "room_type must be string"
    assert isinstance(class_type, str), "class_type must be string"

    room_type = room_type.lower()
    class_type = class_type.lower()
    if class_type == "course":
        return room_type == "course"
    elif class_type == "laboratory":
        return room_type in ["laboratory", "seminar/laboratory"]
    elif class_type == "seminar":
        return room_type in ["course", "laboratory", "seminar", "seminar/laboratory"]
    return False