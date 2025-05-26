export const useDisciplinesStore = defineStore('disciplines', {
  state: () => ({
    disciplines: [] as Discipline[],
    loading: false,
  }),
  actions: {
    async fetchDisciplines() {
      this.loading = true;
      try {
        const response = await useApi('/disciplines', { method: 'GET' }) as Discipline[];

        assert(Array.isArray(response), "fetchDisciplines: API response must be an array");
        assert(response.every(d => d.id !== undefined && typeof d.name === 'string'), "fetchDisciplines: each discipline must have id and name");

        this.disciplines = response;
      } catch (error) {
        console.error('Failed to fetch disciplines:', error);
        this.disciplines = [];
      } finally {
        this.loading = false; 
      }
    }
  }
});
