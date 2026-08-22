import { defineConfig } from 'astro/config';
import remarkDirective from 'remark-directive';
import { remarkCurso } from './src/lib/remark-curso.mjs';

// Casca da plataforma de estudos. Estático; publicável em GitHub Pages.
// O conteúdo é sincronizado do curso (../modulos) por scripts/sync-conteudo.mjs.
export default defineConfig({
  output: 'static',
  server: { port: 4321 },
  markdown: {
    remarkPlugins: [remarkDirective, remarkCurso],
    gfm: true,
  },
});
