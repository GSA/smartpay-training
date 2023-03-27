import { defineConfig } from 'astro/config';

import vue from "@astrojs/vue";

// https://astro.build/config
export default defineConfig({
  base: process.env.BASEURL,
  integrations: [vue()],
  outDir: '../_site'
});