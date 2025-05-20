import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useTimeSlotsStore } from '@/stores/timeSlots.store'

vi.mock('@/composables/useApi', () => ({
  default: vi.fn()
}))

import useApi from '@/composables/useApi'

describe('useTimeSlotsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initial state is correct', () => {
    const store = useTimeSlotsStore()
    expect(store.slots).toEqual([])
    expect(store.loading).toBe(false)
  })

  it('fetchTimeSlots updates state on success', async () => {
    const mockData = [{ id: 1, start_time: '08:00', end_time: '10:00', day: 'Monday' }]
    ;(useApi as any).mockResolvedValue(mockData)

    const store = useTimeSlotsStore()
    await store.fetchTimeSlots()

    expect(store.slots).toEqual(mockData)
    expect(store.loading).toBe(false)
  })

  it('fetchTimeSlots sets empty array on failure', async () => {
    ;(useApi as any).mockRejectedValue(new Error('API error'))

    const store = useTimeSlotsStore()
    await store.fetchTimeSlots()

    expect(store.slots).toEqual([])
    expect(store.loading).toBe(false)
  })
})
