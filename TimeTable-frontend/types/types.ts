export interface Discipline {
  id: number;
  group_id: number;
  year_id: number;
  name: string;
}

export interface Group {
  id: number;
  name: string;
  year_id: number;
}

export interface Teacher {
  id: number;
  name: string;
}

export interface Room {
  id: number;
  name: string;
  room_type: string;
}

export interface Timetable {
  id: number;
  discipline: string;
  teacher: string;
  room: string;
  time_slot: string;
  class_type: string;
}

export interface ClassSession {
  discipline_id: string;
  teacher_id: string;
  room_id: string;
  time_slot_id: string;
  class_type: string;
}