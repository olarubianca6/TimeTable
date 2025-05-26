import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useTeachersStore } from '@/stores/teachers.store'

vi.mock('@/composables/useApi', () => ({
  default: vi.fn()
}))

import useApi from '@/composables/useApi'

describe('useTeachersStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initial state is correct', () => {
    const store = useTeachersStore()
    expect(store.teachers).toEqual([])
    expect(store.loading).toBe(false)
  })

  it('fetchTeachers updates state on success', async () => {
    const mockData = { data: [{ id: 1, name: 'Prof. Ionescu' }] }
    ;(useApi as any).mockResolvedValue(mockData)

    const store = useTeachersStore()
    await store.fetchTeachers()

    expect(store.teachers).toEqual(mockData)
    expect(store.loading).toBe(false)
  })

  it('fetchTeachers sets empty array on failure', async () => {
    ;(useApi as any).mockRejectedValue(new Error('Test API error'))

    const store = useTeachersStore()
    await store.fetchTeachers()

    expect(store.teachers).toEqual([])
    expect(store.loading).toBe(false)
  })
})
