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
  day: string;
  time_slot: string;
  class_type: string;
}

export interface ClassSession {
  discipline_id: number;
  teacher_id: number;
  room_id: number;
  time_slot_id: number;
  class_type: string;
}

export interface TimeSlots {
  id: number;
  day: string;
  start_time: string;
  end_time: string;
}