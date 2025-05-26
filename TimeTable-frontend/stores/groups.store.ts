export const useGroupsStore = defineStore('groups', {
    state: () => ({
      groups: [] as Group[],
      loading: false,
    }),
    actions: {
      async fetchGroups() {
        this.loading = true;
        try {
          const response = await useApi('/groups', { method: 'GET' }) as  Group[];
          
          assert(Array.isArray(response), "fetchGroups: response must be an array");
          response.forEach((g, i) => {
            assert(typeof g.id === 'number', `Group at index ${i} is missing a valid id`);
            assert(typeof g.name === 'string', `Group at index ${i} is missing a name`);
            assert(typeof g.year?.id === 'number', `Group at index ${i} is missing a valid year`);
            assert(typeof g.semian?.id === 'number', `Group at index ${i} is missing a valid semian`);
          });

          this.groups = response;
        } catch (error) {
          console.error('Failed to fetch groups:', error);
          this.groups = [];
        } finally {
          this.loading = false;
        }
      }
    }
});