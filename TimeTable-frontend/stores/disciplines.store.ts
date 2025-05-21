export const useDisciplinesStore = defineStore('disciplines', {
  state: () => ({
    disciplines: [] as Discipline[],
    loading: false,
  }),
  actions: {
    async fetchDisciplines() {
      this.loading = true;
      try {
        const response = await useApi('/disciplines', { method: 'GET' }) as {data: Discipline[]};

        if (response) {
          this.disciplines = response;
        } else {
          this.disciplines = [];
        }
      } catch (error) {
        console.error('Failed to fetch disciplines:', error);
        this.disciplines = [];
      } finally {
        this.loading = false; 
      }
    }
  }
});
