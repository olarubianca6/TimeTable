export const useClassSessionsStore = defineStore('classSessions', {
  state: () => ({
    classSessions: [] as Timetable[],
    loading: false,
  }),
  actions: {
    async fetchClassSessions() {
      this.loading = true;
      try {
        const response = await useApi('/class_sessions', { method: 'GET' }) as { data: Timetable[] };
        if (response) {
          this.classSessions = response.data;
        } else {
          this.classSessions = [];
        }
      } catch (error) {
        console.error('Failed to fetch class sessions:', error);
        this.classSessions = [];
      } finally {
        this.loading = false;
      }
    },

    async fetchClassSession(id: number) {
      this.loading = true;
      try {
        const response = await useApi(`/class_session/${id}`, { method: 'GET' }) as { data: Timetable };
        if (response) {
          return response.data;
        }
      } catch (error) {
        console.error('Failed to fetch class session:', error);
      } finally {
        this.loading = false;
      }
    },

    async addClassSession(data: Partial<ClassSession>) {
      this.loading = true;
      try {
        const response = await useApi('/add_class_session', {
          method: 'POST',
          body: JSON.stringify(data),
        }) as { message: string };
        console.log(response.message);
        await this.fetchClassSessions();
      } catch (error) {
        console.error('Failed to add class session:', error);
      } finally {
        this.loading = false;
      }
    },

    async editClassSession(id: number, data: Partial<Timetable>) {
      this.loading = true;
      try {
        const response = await useApi(`/edit_class_session/${id}`, {
          method: 'PUT',
          body: JSON.stringify(data),
        }) as { message: string };
        console.log(response.message);
        await this.fetchClassSessions();
      } catch (error) {
        console.error('Failed to edit class session:', error);
      } finally {
        this.loading = false;
      }
    },

    async deleteClassSession(id: number) {
      this.loading = true;
      try {
        const response = await useApi(`/delete_class_session/${id}`, { method: 'DELETE' }) as { message: string };
        console.log(response.message);
        await this.fetchClassSessions();
      } catch (error) {
        console.error('Failed to delete class session:', error);
      } finally {
        this.loading = false;
      }
    },
  },
});
