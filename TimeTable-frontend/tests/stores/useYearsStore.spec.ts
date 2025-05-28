import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useYearsStore } from '../../stores/years.store'
import useApi from '@/composables/useApi'

vi.mock('@/composables/useApi', () => ({
  default: vi.fn()
}))


describe('useYearsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initial state is correct', () => {
    const store = useYearsStore()
    expect(store.years).toEqual([])
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('fetchYears updates state on success', async () => {
    const mockData = [{ id: 1, name: '2024' }]
    ;(useApi as any).mockResolvedValue(mockData)

    const store = useYearsStore()
    await store.fetchYears()

    expect(store.years).toEqual(mockData)
    expect(store.error).toBeNull()
    expect(store.loading).toBe(false)
  })

  it('fetchYears sets error on failure', async () => {
    ;(useApi as any).mockRejectedValue(new Error('Test API error'))

    const store = useYearsStore()
    await store.fetchYears()

    expect(store.error).toBe('Failed to load years')
    expect(store.years).toEqual([])
    expect(store.loading).toBe(false)
  })
})
