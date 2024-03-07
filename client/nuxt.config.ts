// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@nuxt/ui", "@nuxtjs/eslint-module"],
  runtimeConfig: {
    public: {
      apiUrl: "http://localhost:8000",
    },
  },
});
