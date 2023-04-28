import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import vue from "@astrojs/vue";
import uswds_links from "./src/plugins/uswds_links";


// https://astro.build/config
export default defineConfig({
  base: process.env.BASEURL,
  integrations: [vue(), mdx()],
  outDir: '../_site',
  markdown: {
    rehypePlugins: [uswds_links]
  }
});