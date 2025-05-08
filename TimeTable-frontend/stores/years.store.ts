export const useYearsStore = defineStore('years', {
  state: () => ({
    years: [] as Years[],
    loading: false,
    error: null as string | null,
  }),
  actions: {
    async fetchYears() {
      this.loading = true;
      try {
        const response = await useApi('/years', { method: 'GET' })as Years[];
        this.years = response;   
      } catch (error) {
        this.error = 'Failed to load years';
      } finally {
        this.loading = false;
      }
    },
  },
});
