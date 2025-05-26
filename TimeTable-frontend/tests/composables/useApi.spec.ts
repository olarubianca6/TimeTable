import { vi, describe, it, expect, beforeEach } from 'vitest'

vi.mock('#app', () => ({
  useRuntimeConfig: () => ({
    public: { apiUrl: 'http://127.0.0.1:5000', baseUrl: ""}
  })
}))

import useApi from '@/composables/useApi'

const $fetchMock = vi.fn() as any
$fetchMock.raw = vi.fn() as any
$fetchMock.create = vi.fn() as any
global.$fetch = $fetchMock

describe('useApi composable', () => {
  beforeEach(() => {
    vi.resetModules()
    vi.clearAllMocks()
  })

  it('should call $fetch with correct arguments and return data on success', async () => {
    const mockResponse = { data: 'ok' }
    $fetchMock.mockResolvedValue(mockResponse)

    const result = await useApi('/rooms', { method: 'GET' })

    expect($fetchMock).toHaveBeenCalledWith('/rooms', expect.objectContaining({
      baseURL: '',
      method: 'GET',
      headers: {}
    }))

    expect(result).toEqual(mockResponse)
  })

  it('should throw the error message from error.data.message on failure', async () => {
    const error = { data: { message: 'Custom error' } }
    $fetchMock.mockRejectedValue(error)

    await expect(useApi('/fail-endpoint', { method: 'GET' })).rejects.toEqual('Custom error')
  })

  it('should throw generic error message if error.data.message is not defined', async () => {
    const error = new Error('Unexpected error')
    $fetchMock.mockRejectedValue(error)

    await expect(useApi('/fail2', { method: 'GET' })).rejects.toEqual('Something went wrong')
  })
})
