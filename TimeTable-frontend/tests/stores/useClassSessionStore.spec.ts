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
    global.alert = vi.fn() 
    console.log = vi.fn() 
  })

  it('initial state is correct', () => {
    const store = useClassSessionsStore()
    expect(store.classSessions).toEqual([])
    expect(store.loading).toBe(false)
  })

  it('fetchClassSessions sets empty array if response is falsy', async () => {
    (useApi as any).mockResolvedValue(undefined);

    const store = useClassSessionsStore();
    await store.fetchClassSessions({});

    expect(store.classSessions).toEqual([]);
    expect(store.loading).toBe(false);
  });
  it('fetchClassSessions sets classSessions with response when response is truthy', async () => {
    const mockData = [{ id: 1, day: 'Monday', discipline: 'Math' }];
    (useApi as any).mockResolvedValue(mockData);

    const store = useClassSessionsStore();
    await store.fetchClassSessions({ year_id: 2024 });

    expect(store.classSessions).toEqual(mockData);
    expect(store.loading).toBe(false);
  });
  it('fetchClassSessions sets classSessions to empty array and calls alert on error', async () => {
    (useApi as any).mockRejectedValue(new Error('API failure'));

    const store = useClassSessionsStore();

    global.alert = vi.fn();

    await store.fetchClassSessions(undefined);

    expect(global.alert).toHaveBeenCalledWith(expect.any(Error));
    expect(store.classSessions).toEqual([]);
    expect(store.loading).toBe(false);
    });


  it('fetchClassSession logs error and sets loading false on failure', async () => {
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    (useApi as any).mockRejectedValue(new Error('Fetch session failed'));

    const store = useClassSessionsStore();
    const result = await store.fetchClassSession(123);

    expect(result).toBeUndefined();
    expect(consoleErrorSpy).toHaveBeenCalledWith('Failed to fetch class session:', expect.any(Error));
    expect(store.loading).toBe(false);

    consoleErrorSpy.mockRestore();
  });

  it('alerts error on addClassSession failure', async () => {
    (useApi as any).mockRejectedValue(new Error('Add failed'));
  
    const store = useClassSessionsStore();

    await store.addClassSession({ discipline_id: 1 });

    expect(global.alert).toHaveBeenCalledWith(expect.any(Error));
    expect(store.loading).toBe(false);
  });

  it('alerts error on editClassSession failure', async () => {
    (useApi as any).mockRejectedValue(new Error('Edit failed'));
  
    const store = useClassSessionsStore();

    await store.editClassSession(1, { discipline: 'X' });

    expect(global.alert).toHaveBeenCalledWith(expect.any(Error));
    expect(store.loading).toBe(false);
  });

  it('alerts error on deleteClassSession failure', async () => {
    (useApi as any).mockRejectedValue(new Error('Delete failed'));
  
    const store = useClassSessionsStore();

    await store.deleteClassSession(1);

    expect(global.alert).toHaveBeenCalledWith(expect.any(Error));
    expect(store.loading).toBe(false);
  });


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
