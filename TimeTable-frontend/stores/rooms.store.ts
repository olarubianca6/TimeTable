export const useRoomsStore = defineStore('rooms', {
  state: () => ({
    rooms: [] as Room[],
    loading: false,
  }),
  actions: {
    async fetchRooms() {
      this.loading = true;
      try {
        const response = await useApi('/rooms', { method: 'GET' }) as Room[];

        assert(Array.isArray(response), "fetchRooms: response must be an array");
        response.forEach((room, index) => {
          assert(typeof room.id === 'number', `Room at index ${index} must have a numeric id`);
          assert(typeof room.name === 'string', `Room at index ${index} must have a name`);
          assert(typeof room.room_type === 'string', `Room at index ${index} must have a room_type`);
        });

        this.rooms = response;
      } catch (error) {
        console.error('Failed to fetch rooms:', error);
        this.rooms = [];
      } finally {
        this.loading = false;
      }
    }
  }
});
