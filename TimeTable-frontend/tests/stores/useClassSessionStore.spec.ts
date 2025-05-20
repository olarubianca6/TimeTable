import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useClassSessionsStore } from '@/stores/classSessions.store'

vi.mock('@/composables/useApi', () => ({
  default: vi.fn()
}))

import useApi from '@/composables/useApi'

describe('useClassSessionsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    global.alert = vi.fn() // mock alert globally
    console.log = vi.fn()  // optional: suppress log output
  })

  it('initial state is correct', () => {
    const store = useClassSessionsStore()
    expect(store.classSessions).toEqual([])
    expect(store.loading).toBe(false)
  })

  it('fetchClassSessions updates state on success', async () => {
    const mockData = [{ id: 1, day: 'Monday', discipline: 'Math' }]
    ;(useApi as any).mockResolvedValue(mockData)

    const store = useClassSessionsStore()
    await store.fetchClassSessions({ year_id: 2024 })

    expect(store.classSessions).toEqual(mockData)
    expect(store.loading).toBe(false)
  })

  it('fetchClassSessions sets error fallback', async () => {
    ;(useApi as any).mockRejectedValue(new Error('API error'))

    const store = useClassSessionsStore()
    await store.fetchClassSessions(undefined)

    expect(store.classSessions).toEqual([])
    expect(store.loading).toBe(false)
    expect(global.alert).toHaveBeenCalled()
  })

  it('fetchClassSession returns single session', async () => {
    const mockData = { data: { id: 1, day: 'Tuesday', discipline: 'Physics' } }
    ;(useApi as any).mockResolvedValue(mockData)

    const store = useClassSessionsStore()
    const result = await store.fetchClassSession(1)

    expect(result).toEqual(mockData.data)
    expect(store.loading).toBe(false)
  })

  it('addClassSession calls fetchClassSessions', async () => {
    ;(useApi as any).mockResolvedValue({ message: 'Added' })

    const store = useClassSessionsStore()
    store.fetchClassSessions = vi.fn()

    await store.addClassSession({ discipline_id: 1 })
    expect(store.fetchClassSessions).toHaveBeenCalled()
    expect(store.loading).toBe(false)
  })

  it('editClassSession calls fetchClassSessions', async () => {
    ;(useApi as any).mockResolvedValue({ message: 'Edited' })

    const store = useClassSessionsStore()
    store.fetchClassSessions = vi.fn()

    await store.editClassSession(1, { discipline: 'Updated' })
    expect(store.fetchClassSessions).toHaveBeenCalled()
    expect(store.loading).toBe(false)
  })

  it('deleteClassSession calls fetchClassSessions', async () => {
    ;(useApi as any).mockResolvedValue({ message: 'Deleted' })

    const store = useClassSessionsStore()
    store.fetchClassSessions = vi.fn()

    await store.deleteClassSession(1)
    expect(store.fetchClassSessions).toHaveBeenCalled()
    expect(store.loading).toBe(false)
  })
})
