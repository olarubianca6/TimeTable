import tailwindcss from "@tailwindcss/vite";
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxt/eslint', '@nuxt/icon', '@nuxt/ui', '@pinia/nuxt', '@nuxt/test-utils/module'],
  runtimeConfig: {
    public: {
      baseUrl: process.env.BASE_URL,
      apiUrl: process.env.API_URL,
    },
  },

  ssr: false,

  imports: {
    dirs: ["store/.ts", "types/**/.ts", "types/*.ts"],
  },

  css: ["~/assets/css/main.css"],
  vite: {
    plugins: [tailwindcss()],
  },

  components: [{ path: "~/components", pathPrefix: false }],
})