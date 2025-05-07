export const useRoomsStore = defineStore('rooms', {
  state: () => ({
    rooms: [] as Room[],
    loading: false,
  }),
  actions: {
    async fetchRooms() {
      this.loading = true;
      try {
        const response = await useApi('/rooms', { method: 'GET' }) as { data: Room[] };

        if (response) {
          this.rooms = response;
        } else {
          this.rooms = [];
        }
      } catch (error) {
        console.error('Failed to fetch rooms:', error);
        this.rooms = [];
      } finally {
        this.loading = false;
      }
    }
  }
});
