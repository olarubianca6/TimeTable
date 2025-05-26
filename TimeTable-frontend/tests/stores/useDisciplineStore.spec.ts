import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useDisciplinesStore } from '@/stores/disciplines.store'

vi.mock('@/composables/useApi', () => ({
  default: vi.fn()
}))

import useApi from '@/composables/useApi'

describe('useDisciplinesStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initial state is correct', () => {
    const store = useDisciplinesStore()
    expect(store.disciplines).toEqual([])
    expect(store.loading).toBe(false)
  })

  it('fetchDisciplines updates state on success', async () => {
    const mockData = { data: [{ id: 1, name: 'Mathematics' }] }
    ;(useApi as any).mockResolvedValue(mockData)

    const store = useDisciplinesStore()
    await store.fetchDisciplines()

    expect(store.disciplines).toEqual(mockData)
    expect(store.loading).toBe(false)
  })

  it('fetchDisciplines sets empty array on failure', async () => {
    ;(useApi as any).mockRejectedValue(new Error('Test API error'))

    const store = useDisciplinesStore()
    await store.fetchDisciplines()

    expect(store.disciplines).toEqual([])
    expect(store.loading).toBe(false)
  })
})
