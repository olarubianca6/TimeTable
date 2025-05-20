import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useGroupsStore } from '@/stores/groups.store'

vi.mock('@/composables/useApi', () => ({
  default: vi.fn()
}))

import useApi from '@/composables/useApi'

describe('useGroupsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initial state is correct', () => {
    const store = useGroupsStore()
    expect(store.groups).toEqual([])
    expect(store.loading).toBe(false)
  })

  it('fetchGroups updates state on success', async () => {
    const mockData = { data: [{ id: 1, name: 'G1', semian: 1 }] }
    ;(useApi as any).mockResolvedValue(mockData)

    const store = useGroupsStore()
    await store.fetchGroups()

    expect(store.groups).toEqual(mockData)
    expect(store.loading).toBe(false)
  })

  it('fetchGroups sets empty array on failure', async () => {
    ;(useApi as any).mockRejectedValue(new Error('API error'))

    const store = useGroupsStore()
    await store.fetchGroups()

    expect(store.groups).toEqual([])
    expect(store.loading).toBe(false)
  })
})
