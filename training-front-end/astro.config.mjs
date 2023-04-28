import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import vue from "@astrojs/vue";
import uswds_links from "./src/plugins/uswds_links";

import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  base: '/',
  site: process.env.BASEURL,
  integrations: [vue(), mdx(), sitemap()],
  outDir: '../_site',
  markdown: {
    rehypePlugins: [uswds_links]
  }
});