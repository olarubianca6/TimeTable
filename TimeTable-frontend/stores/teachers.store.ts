export const useTeachersStore = defineStore('teachers', {
  state: () => ({
    teachers: [] as Teacher[],
    loading: false,
  }),
  actions: {
    async fetchTeachers() {
      this.loading = true;
      try {
        const response = await useApi('/teachers', { method: 'GET' }) as { data: Teacher[]};

        if (response) {
          this.teachers = response;
        } else {
          this.teachers = [];
        }
      } catch (error) {
        console.error('Failed to fetch teachers:', error);
        this.teachers = [];
      } finally {
        this.loading = false;
      }
    }
  }
});
