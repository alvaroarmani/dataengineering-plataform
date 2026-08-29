// Sincroniza o conteúdo do curso (../modulos) para a plataforma Next.
// - Compila Markdown -> HTML no build (preprocess MyST + remark-directive + remark-curso + gfm + rehype-raw).
// - Gera src/data/curso.json (eixos -> módulos -> unidades, com html e cards).
// - Copia a instância JupyterLite para public/lite (uma vez).
// Roda antes de dev/build (ver package.json).
import fs from 'node:fs';
import path from 'node:path';
import url from 'node:url';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkDirective from 'remark-directive';
import remarkRehype from 'remark-rehype';
import rehypeRaw from 'rehype-raw';
import rehypeStringify from 'rehype-stringify';
import { visit, SKIP } from 'unist-util-visit';
import { remarkCurso } from '../src/lib/remark-curso.mjs';
import { preprocessMyst } from '../src/lib/preprocess-myst.mjs';

// Envolve cada <table> num <div class="tbl-scroll"> para rolagem horizontal confiável no
// mobile (evita que linhas largas estourem a viewport e disparem o "encaixar por largura").
function rehypeWrapTables() {
  return (tree) => {
    visit(tree, 'element', (node, index, parent) => {
      if (node.tagName !== 'table' || !parent || typeof index !== 'number') return;
      const jaEnvolto = parent.tagName === 'div'
        && [].concat(parent.properties?.className || []).includes('tbl-scroll');
      if (jaEnvolto) return;
      parent.children[index] = {
        type: 'element',
        tagName: 'div',
        properties: { className: ['tbl-scroll'] },
        children: [node],
      };
      return [SKIP, index + 1];
    });
  };
}

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const WEB = path.resolve(__dirname, '..');
const RAIZ = path.resolve(WEB, '..');
const MODULOS = path.join(RAIZ, 'modulos');
const OUT_DATA = path.join(WEB, 'src', 'data');
const LITE_SRC = path.join(RAIZ, '_build', 'html', 'lite');
const LITE_DST = path.join(WEB, 'public', 'lite');

const proc = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkDirective)
  .use(remarkCurso)
  .use(remarkRehype, { allowDangerousHtml: true })
  .use(rehypeRaw)
  .use(rehypeWrapTables)
  .use(rehypeStringify, { allowDangerousHtml: true });

function mdToHtml(md) {
  return String(proc.processSync(preprocessMyst(md)));
}
function tituloDe(md, fallback) {
  const m = md.match(/^#\s+(.+)$/m);
  return m ? m[1].replace(/[🎯💡🔎⚠️💼🧠🎤🚀📚🃏✨🏭📖]/gu, '').trim() || fallback : fallback;
}
function tipoDe(base) {
  if (base === 'index') return 'index';
  if (base.startsWith('teoria')) return 'teoria';
  if (base.startsWith('lab')) return 'lab';
  if (base.startsWith('exercicio')) return 'exercicio';
  if (base === 'recursos') return 'recursos';
  if (base === 'flashcards') return 'flashcards';
  return 'outro';
}
const ORDEM = { teoria: 1, lab: 2, exercicio: 3, flashcards: 4, recursos: 5, outro: 6 };

function parseCards(md) {
  const re = /^-\s*\*\*P:\*\*\s*(.+?)\s*\/\s*\*\*R:\*\*\s*(.+)$/gm;
  const cards = [];
  let m;
  while ((m = re.exec(md)) !== null) cards.push({ p: m[1].trim(), r: m[2].trim() });
  return cards;
}

function mkdirp(p) { fs.mkdirSync(p, { recursive: true }); }

function main() {
  // Deploy externo (ex.: Vercel com Root Directory = web) não tem acesso a ../modulos.
  // Nesse caso, usamos o conteúdo já VERSIONADO (src/content + src/data/curso.json).
  if (!fs.existsSync(MODULOS) || !fs.existsSync(path.join(RAIZ, 'progresso.json'))) {
    console.log('[sync] fonte ../modulos ausente — usando conteúdo versionado (build externo).');
    return;
  }
  const progresso = JSON.parse(fs.readFileSync(path.join(RAIZ, 'progresso.json'), 'utf8'));
  mkdirp(OUT_DATA);

  const pastas = fs.readdirSync(MODULOS).filter(
    (f) => fs.statSync(path.join(MODULOS, f)).isDirectory() && /^\d\d-/.test(f)
  );
  const porNumero = {};
  pastas.forEach((p) => { porNumero[p.slice(0, 2)] = p; });

  const eixos = [];
  for (const eixo of progresso.eixos) {
    const modulos = [];
    for (const mod of eixo.modulos) {
      const num = String(mod.id).replace(/\D/g, '').padStart(2, '0');
      const pasta = porNumero[num];
      if (!pasta) continue;
      const dir = path.join(MODULOS, pasta);
      const arquivos = fs.readdirSync(dir).filter((f) => f.endsWith('.md') || f.endsWith('.ipynb'));

      let indexHtml = '';
      const unidades = [];
      for (const arq of arquivos) {
        const base = arq.replace(/\.(md|ipynb)$/, '');
        const tipo = tipoDe(base);
        if (arq.endsWith('.ipynb')) {
          unidades.push({
            tipo: 'lab', base,
            titulo: 'Lab — ' + base.replace(/^lab-\d+-/, '').replace(/-/g, ' '),
            isLab: true, href: `/lite/lab/index.html?path=${arq}`,
          });
          continue;
        }
        const raw = fs.readFileSync(path.join(dir, arq), 'utf8');
        const titulo = tituloDe(raw, base);
        if (tipo === 'index') { indexHtml = mdToHtml(raw); continue; }
        const unidade = { tipo, base, titulo, isLab: false, html: mdToHtml(raw) };
        if (tipo === 'flashcards') unidade.cards = parseCards(raw);
        unidades.push(unidade);
      }
      unidades.sort((a, b) => (ORDEM[a.tipo] - ORDEM[b.tipo]) || a.base.localeCompare(b.base));
      modulos.push({ id: mod.id, nome: mod.nome, ch: mod.ch, pasta, indexHtml, unidades });
    }
    eixos.push({ id: eixo.id, nome: eixo.nome, modulos });
  }

  fs.writeFileSync(path.join(OUT_DATA, 'curso.json'), JSON.stringify({ eixos }), 'utf8');

  // Copia o JupyterLite uma vez (é grande; não re-copia se já existe).
  if (fs.existsSync(LITE_SRC) && !fs.existsSync(LITE_DST)) {
    fs.cpSync(LITE_SRC, LITE_DST, { recursive: true });
    console.log('lite copiado para public/lite');
  }

  const nMods = eixos.reduce((n, e) => n + e.modulos.length, 0);
  const nUn = eixos.reduce((n, e) => n + e.modulos.reduce((m, md) => m + md.unidades.length, 0), 0);
  console.log(`sync ok: ${eixos.length} eixos, ${nMods} módulos, ${nUn} unidades.`);
}

main();
