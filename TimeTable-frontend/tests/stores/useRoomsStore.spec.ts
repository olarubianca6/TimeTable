import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useRoomsStore } from '@/stores/rooms.store'

vi.mock('@/composables/useApi', () => ({
  default: vi.fn()
}))

import useApi from '@/composables/useApi'

describe('useRoomsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initial state is correct', () => {
    const store = useRoomsStore()
    expect(store.rooms).toEqual([])
    expect(store.loading).toBe(false)
  })

  it('fetchRooms updates state on success', async () => {
    const mockData = { data: [{ id: 1, name: 'Room A' }] }
    ;(useApi as any).mockResolvedValue(mockData)

    const store = useRoomsStore()
    await store.fetchRooms()

    expect(store.rooms).toEqual(mockData)
    expect(store.loading).toBe(false)
  })

  it('fetchRooms sets empty array on failure', async () => {
    ;(useApi as any).mockRejectedValue(new Error('API error'))

    const store = useRoomsStore()
    await store.fetchRooms()

    expect(store.rooms).toEqual([])
    expect(store.loading).toBe(false)
  })
})
