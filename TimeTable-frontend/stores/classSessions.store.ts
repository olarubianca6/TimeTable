export const useClassSessionsStore = defineStore('classSessions', {
  state: () => ({
    classSessions: [] as Timetable[],
    loading: false,
  }),
  actions: {
    async fetchClassSessions(payload: ClassSessionPayload | undefined) {
      this.loading = true;
      try {
        const response = await useApi(`/class_sessions`, 
          { 
            method: 'GET', 
            params: payload,
          }) as  Timetable[] ;
        assert(Array.isArray(response), "fetchClassSessions: API must return an array");
        assert(response.every(item => item.id !== undefined), "fetchClassSessions: every item must have an ID");

        if (response) {
          this.classSessions = response;
        } else {
          this.classSessions = [];
        }
      } catch (error) {
        console.error(error);
        
        this.classSessions = [];
      } finally {
        this.loading = false;
      }
    },
    
    async fetchClassSession(id: number) {
      this.loading = true;
      try {
        assert(Number.isInteger(id) && id > 0, "fetchClassSession: id must be a positive integer");

        const response = await useApi(`/class_session/${id}`, { method: 'GET' }) as { data: Timetable };
        assert(!!response && !!response.data, "fetchClassSession: expected response.data");
        return response.data;
      } catch (error) {
        console.error('Failed to fetch class session:', error);
      } finally {
        this.loading = false;
      }
    },

    async addClassSession(data: Partial<ClassSession>) {
      this.loading = true;
      try {
        assert(data !== undefined, "addClassSession: data must be provided");
        assert(typeof data.discipline_id === 'number', "addClassSession: discipline_id must be a number");
        assert(typeof data.teacher_id === 'number', "addClassSession: teacher_id must be a number");

        const response = await useApi('/add_class_session', {
          method: 'POST',
          body: JSON.stringify(data),
        }) as { message: string, error: string };
        
        await this.fetchClassSessions({});
        assert(response !== undefined, "addClassSession: no response from API");

        if(response.error) {
          alert(response.error)
        }
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async editClassSession(id: number, data: Partial<Timetable>) {
      this.loading = true;
      try {
        assert(Number.isInteger(id) && id > 0, "editClassSession: id must be a positive integer");
        assert(data !== undefined, "editClassSession: data must be provided");

        const response = await useApi(`/edit_class_session/${id}`, {
          method: 'PUT',
          body: JSON.stringify(data),
        }) as { message: string, error: string };
        
        assert(response !== undefined, "editClassSession: no response from API");

        if (response.error) {
          alert(response.error);
        } else {
          await this.fetchClassSessions();
        }
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async deleteClassSession(id: number) {
      this.loading = true;
      try {
        assert(Number.isInteger(id) && id > 0, "deleteClassSession: id must be a positive integer");
        const response = await useApi(`/delete_class_session/${id}`, { method: 'DELETE' }) as { message: string, error: string };
   
        assert(response !== undefined, "deleteClassSession: no response from API");

        if (response.error) {
          alert(response.error);
        } else {
          await this.fetchClassSessions();
        }
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
  },
});
