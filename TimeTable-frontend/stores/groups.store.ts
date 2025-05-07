export const useGroupsStore = defineStore('groups', {
    state: () => ({
      groups: [] as Group[],
      loading: false,
    }),
    actions: {
      async fetchGroups() {
        this.loading = true;
        try {
            const response = await useApi('/groups', { method: 'GET' }) as {data: Group[]};
  
          if (response) {
            this.groups = response;
          } else {
            this.groups = [];
          }
        } catch (error) {
          console.error('Failed to fetch groups:', error);
          this.groups = [];
        } finally {
          this.loading = false;
        }
      }
    }
});