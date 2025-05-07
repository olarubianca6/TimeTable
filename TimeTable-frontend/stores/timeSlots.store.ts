export const useTimeSlotsStore = defineStore('timeSlotsStore', {
    state: () => ({
      slots: [] as TimeSlots[],
      loading: false,
    }),
    actions: {
      async fetchTimeSlots() {
        this.loading = true;
        try {
          const response = await useApi('/time_slots', { method: 'GET' }) as TimeSlots[];
  
          if (response) {
            this.slots = response;
          } else {
            this.slots = [];
          }
        } catch (error) {
          console.error('Failed to fetch slots:', error);
          this.slots = [];
        } finally {
          this.loading = false; 
        }
      }
    }
  });
  