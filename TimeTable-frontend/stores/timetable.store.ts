export const useTimetableStore = defineStore('timetable', {
  state: () => ({
    timetable: [] as Timetable[],
    loading: false,
  }),
  actions: {
    async fetchTimetable() {
      this.loading = true;
      try {
        const response = await useApi('/timetable', { method: 'GET' })as { data: Timetable[] };

        if (response) {
          this.timetable = response;
        } else {
          this.timetable = [];
        }
      } catch (error) {
        console.error('Failed to fetch timetable:', error);
        this.timetable = [];
      } finally {
        this.loading = false;
      }
    }
  }
});
