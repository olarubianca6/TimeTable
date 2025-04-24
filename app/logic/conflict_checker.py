def room_conflict(existing_entries, new_entry):
    return any(
        e.room_id == new_entry.room_id and
        e.time_slot_id == new_entry.time_slot_id
        for e in existing_entries
    )

def teacher_conflict(existing_entries, new_entry):
    new_teachers = {dt.teacher_id for dt in new_entry.discipline.teacher_links}
    for e in existing_entries:
        if e.time_slot_id == new_entry.time_slot_id:
            existing_teachers = {dt.teacher_id for dt in e.discipline.teacher_links}
            if new_teachers & existing_teachers:
                return True
    return False