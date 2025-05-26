import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useTimetableStore } from '@/stores/timetable.store'

vi.mock('@/composables/useApi', () => ({
  default: vi.fn()
}))

import useApi from '@/composables/useApi'

describe('useTimetableStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initial state is correct', () => {
    const store = useTimetableStore()
    expect(store.timetable).toEqual([])
    expect(store.loading).toBe(false)
  })

  it('fetchTimetable updates state on success', async () => {
    const mockData = { data: [{ id: 1, day: 'Monday', time: '08:00', discipline: 'Math' }] }
    ;(useApi as any).mockResolvedValue(mockData)

    const store = useTimetableStore()
    await store.fetchTimetable()

    expect(store.timetable).toEqual(mockData)
    expect(store.loading).toBe(false)
  })

  it('fetchTimetable sets empty array on failure', async () => {
    ;(useApi as any).mockRejectedValue(new Error('Test API error'))

    const store = useTimetableStore()
    await store.fetchTimetable()

    expect(store.timetable).toEqual([])
    expect(store.loading).toBe(false)
  })
})
