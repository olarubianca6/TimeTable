export const useTeachersStore = defineStore('teachers', {
  state: () => ({
    teachers: [] as Teacher[],
    loading: false,
  }),
  actions: {
    async fetchTeachers() {
      this.loading = true;
      try {
        const response = await useApi('/teachers', { method: 'GET' }) as Teacher[];

        assert(Array.isArray(response), "fetchTeachers: response must be an array");
        response.forEach((teacher, index) => {
          assert(typeof teacher.id === 'number', `Teacher at index ${index} must have a numeric id`);
          assert(typeof teacher.name === 'string', `Teacher at index ${index} must have a name`);
        });

        this.teachers = response;
      } catch (error) {
        console.error('Failed to fetch teachers:', error);
        this.teachers = [];
      } finally {
        this.loading = false;
      }
    }
  }
});
