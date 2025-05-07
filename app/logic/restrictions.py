def valid_class_time(day, hour):
    return day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] and 8 <= hour <= 20

def match_room_class_type(room_type, class_type):
    if class_type == "Course":
        return room_type == "Course"
    elif class_type == "Laboratory":
        return room_type in ["Laboratory", "Seminar/Laboratory"]
    elif class_type == "Seminar":
        return room_type in ["Course", "Laboratory", "Seminar", "Seminar/Laboratory"]
    return False