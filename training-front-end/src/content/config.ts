import { z, defineCollection } from 'astro:content';

// Define types for content collections
const trainingCollection = defineCollection({
  schema: z.object({
    title: z.string(),
    order: z.number(),
  }),
});
export const collections = {
  'training_travel': trainingCollection,
};
