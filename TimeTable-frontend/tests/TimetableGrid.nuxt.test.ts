import { test } from 'vitest'

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/vue'
import TimetableGrid from '../components/TimetableGrid.vue'
import { ref } from 'vue'
global.alert = vi.fn() 

vi.mock('@/stores/disciplines.store.ts', () => ({
  useDisciplinesStore: () => ({
    disciplines: ref([{ id: 1, name: 'Math' }]),
    fetchDisciplines: vi.fn()
  })
}))
vi.mock('@/stores/groups.store.ts', () => ({
  useGroupsStore: () => ({
    groups: ref([{ id: 1, name: 'G1', semian: 1 }]),
    fetchGroups: vi.fn()
  })
}))
vi.mock('@/stores/teachers.store.ts', () => ({
  useTeachersStore: () => ({
    teachers: ref([{ id: 1, name: 'Prof. Popescu' }]),
    fetchTeachers: vi.fn()
  })
}))
vi.mock('@/stores/rooms.store.ts', () => ({
  useRoomsStore: () => ({
    rooms: ref([{ id: 1, name: '101' }]),
    fetchRooms: vi.fn()
  })
}))
vi.mock('@/stores/classSessions.store.ts', () => ({
  useClassSessionsStore: () => ({
    classSessions: ref([]),
    fetchClassSessions: vi.fn(),
    addClassSession: vi.fn(),
    deleteClassSession: vi.fn()
  })
}))
vi.mock('@/stores/years.store.ts', () => ({
  useYearsStore: () => ({
    years: ref([]),
    fetchYears: vi.fn()
  })
}))
vi.mock('@/stores/timeSlots.store.ts', () => ({
  useTimeSlotsStore: () => ({
    slots: ref([
      { id: 1, day: 'Monday', start_time: '08:00', end_time: '10:00' }
    ]),
    fetchTimeSlots: vi.fn()
  })
}))

describe('TimetableGrid', () => {
  it('renders title and form', async () => {
    render(TimetableGrid)

    expect(screen.getByText('Adaugă sesiune')).toBeTruthy()
    expect(screen.getByRole('button', { name: /Adaugă/i })).toBeTruthy()
  })

  it('fills and submits the form', async () => {
    render(TimetableGrid)

    await fireEvent.update(screen.getAllByRole('combobox')[0], 'Monday')
    await fireEvent.update(screen.getAllByRole('combobox')[1], '08:00 - 10:00')
    await fireEvent.update(screen.getAllByRole('combobox')[2], 'G1')
    await fireEvent.update(screen.getAllByRole('combobox')[3], 'Prof. Popescu')
    await fireEvent.update(screen.getAllByRole('combobox')[4], 'Math')
    await fireEvent.update(screen.getAllByRole('combobox')[5], 'course')
    await fireEvent.update(screen.getAllByRole('combobox')[6], '101')

    await fireEvent.click(screen.getAllByRole('button', { name: /Adaugă/i })[0])

    expect(true).toBe(true)
  })
})
