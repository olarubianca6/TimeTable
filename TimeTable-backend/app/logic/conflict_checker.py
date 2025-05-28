from app.models import Discipline


def room_conflict(existing_entries, new_entry):
    assert existing_entries is not None, "existing_entries must not be none"
    assert new_entry is not None, "new_entry must not be none"
    assert new_entry.room_id is not None, "new_entry must have room_id"
    assert new_entry.time_slot_id is not None, "new_entry must have time_slot_id"
    return any(
        e.room_id == new_entry.room_id and
        e.time_slot_id == new_entry.time_slot_id
        for e in existing_entries
    )


def teacher_conflict(existing_entries, new_entry):
    assert existing_entries is not None, "existing_entries must not be none"
    assert new_entry is not None, "new_entry must not be none"
    assert hasattr(new_entry, 'discipline') and new_entry.discipline is not None, "new_entry must have a discipline"
    assert hasattr(new_entry.discipline, 'teacher_links'), "discipline must have teacher_links"

    new_teachers = {dt.teacher_id for dt in new_entry.discipline.teacher_links}
    for e in existing_entries:
        if e.time_slot_id == new_entry.time_slot_id:
            existing_teachers = {dt.teacher_id for dt in e.discipline.teacher_links}
            if new_teachers & existing_teachers:
                return True
    return False


def group_conflict(existing_entries, new_entry):
    assert existing_entries is not None, "existing_entries must not be none"
    assert new_entry is not None, "new_entry must not be none"
    assert new_entry.discipline_id is not None, "new_entry must have discipline_id"

    new_discipline = Discipline.query.get(new_entry.discipline_id)
    assert new_discipline is not None, "discipline must not be none"

    if not new_discipline.groups:
        return False

    new_group_ids = {g.id for g in new_discipline.groups}
    for e in existing_entries:
        if e.time_slot_id == new_entry.time_slot_id:
            existing_group_ids = {e.group_id}
            if new_group_ids & existing_group_ids:
                return True
    return False


def semian_conflict(existing_entries, new_entry):
    assert existing_entries is not None, "existing_entries must not be none"
    assert new_entry is not None, "new_entry must not be none"
    assert new_entry.semian_id is not None, "new_entry must have semian_id"
    assert new_entry.time_slot_id is not None, "new_entry must have time_slot_id"

    new_semian_id = new_entry.semian_id
    for e in existing_entries:
        if e.time_slot_id == new_entry.time_slot_id and e.semian_id == new_semian_id:
            return True
    return False
