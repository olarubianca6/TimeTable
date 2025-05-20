export const useSessionStore = defineStore('session', {
    state: () => ({
        sessions: [] as any[]
      }),
      actions: {
        actions: {
            async fetchSessions(filters = {}) {
             
            },
            async saveSession(session: any) {
              
            }
          }
}})