import { defineConfig } from 'astro/config';
import { remarkHeadingId } from 'remark-custom-heading-id';
import mdx from '@astrojs/mdx';
import vue from "@astrojs/vue";
import { processLinksPlugin } from "./src/plugins/uswds_links";

import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  site: 'https://training.smartpay.gsa.gov',
  base: process.env.BASEURL,
  integrations: [vue(), mdx(), sitemap()],
  outDir: '../_site',
  markdown: {
    remarkPlugins: [remarkHeadingId],
    rehypePlugins: [processLinksPlugin]
  },
  trailingSlash: 'always',
});