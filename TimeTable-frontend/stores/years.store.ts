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
        assert(Array.isArray(response), "fetchYears: response must be an array");
        response.forEach((year, index) => {
          assert(typeof year.id === 'number', `Year at index ${index} must have a numeric id`);
          assert(typeof year.name === 'string', `Year at index ${index} must have a valid name`);
        });

        this.years = response;
        this.error = null;
      } catch (error) {
        this.error = 'Failed to load years';
      } finally {
        this.loading = false;
      }
    },
  },
});
