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
  
          assert(Array.isArray(response), "fetchTimeSlots: response must be an array");
          response.forEach((slot, index) => {
            assert(typeof slot.id === 'number', `TimeSlot at index ${index} must have a numeric id`);
            assert(typeof slot.day === 'string', `TimeSlot at index ${index} must have a valid day`);
            assert(typeof slot.start_time === 'string', `TimeSlot at index ${index} must have a start_time`);
            assert(typeof slot.end_time === 'string', `TimeSlot at index ${index} must have an end_time`);
          });

          this.slots = response;
        } catch (error) {
          console.error('Failed to fetch slots:', error);
          this.slots = [];
        } finally {
          this.loading = false; 
        }
      }
    }
  });
  