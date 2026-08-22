import { defineCollection, z } from 'astro:content';

// Coleção gerada pelo sync (scripts/sync-conteudo.mjs) a partir de ../modulos.
const aulas = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    modulo: z.string(),
    moduloNome: z.string(),
    moduloId: z.string(),
    eixo: z.number(),
    tipo: z.string(),
  }),
});

export const collections = { aulas };
