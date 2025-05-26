export const useTimetableStore = defineStore('timetable', {
  state: () => ({
    timetable: [] as Timetable[],
    loading: false,
  }),
  actions: {
    async fetchTimetable() {
      this.loading = true;
      try {
        const response = await useApi('/timetable', { method: 'GET' }) as Timetable[];

        assert(Array.isArray(response), "fetchTimetable: response must be an array");
        response.forEach((entry, index) => {
          assert(typeof entry.id === 'number', `Timetable entry at index ${index} must have a numeric id`);
          assert(typeof entry.discipline === 'string', `Timetable entry at index ${index} must have a discipline`);
          assert(typeof entry.teacher === 'string', `Timetable entry at index ${index} must have a teacher`);
          assert(typeof entry.room === 'string', `Timetable entry at index ${index} must have a room`);
          assert(typeof entry.day === 'string', `Timetable entry at index ${index} must have a valid day`);
          assert(typeof entry.time_slot === 'string', `Timetable entry at index ${index} must have a valid time_slot`);
          assert(typeof entry.class_type === 'string', `Timetable entry at index ${index} must have a class_type`);
        });

        this.timetable = response;
      } catch (error) {
        console.error('Failed to fetch timetable:', error);
        this.timetable = [];
      } finally {
        this.loading = false;
      }
    }
  }
});
