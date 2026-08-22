// Sincroniza o conteúdo do curso (Markdown em ../modulos) para a plataforma Astro.
// - Transforma diretivas MyST (via preprocessMyst) e escreve na coleção src/content/aulas.
// - Gera src/data/curso.json (eixos → módulos → unidades) para Trilha/Módulo.
// Rode: npm run sync  (roda automaticamente antes de dev/build)
import fs from 'node:fs';
import path from 'node:path';
import url from 'node:url';
import { preprocessMyst } from '../src/lib/preprocess-myst.mjs';

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const PLATAFORMA = path.resolve(__dirname, '..');
const RAIZ = path.resolve(PLATAFORMA, '..');
const MODULOS = path.join(RAIZ, 'modulos');
const OUT_CONTENT = path.join(PLATAFORMA, 'src', 'content', 'aulas');
const OUT_DATA = path.join(PLATAFORMA, 'src', 'data');

function rmrf(p) { if (fs.existsSync(p)) fs.rmSync(p, { recursive: true, force: true }); }
function mkdirp(p) { fs.mkdirSync(p, { recursive: true }); }

function tituloDe(md, fallback) {
  const m = md.match(/^#\s+(.+)$/m);
  return m ? m[1].trim() : fallback;
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

const ORDEM = { index: 0, teoria: 1, lab: 2, exercicio: 3, flashcards: 4, recursos: 5, outro: 6 };

function main() {
  const progresso = JSON.parse(fs.readFileSync(path.join(RAIZ, 'progresso.json'), 'utf8'));

  rmrf(OUT_CONTENT); mkdirp(OUT_CONTENT); mkdirp(OUT_DATA);

  const pastas = fs.readdirSync(MODULOS).filter((f) =>
    fs.statSync(path.join(MODULOS, f)).isDirectory() && /^\d\d-/.test(f)
  );
  const porNumero = {}; // "01" -> pasta
  pastas.forEach((p) => { porNumero[p.slice(0, 2)] = p; });

  const eixosOut = [];
  for (const eixo of progresso.eixos) {
    const modsOut = [];
    for (const mod of eixo.modulos) {
      const num = String(mod.id).replace(/\D/g, '').padStart(2, '0');
      const pasta = porNumero[num];
      if (!pasta) continue; // ex.: TCC (fora de modulos/) — tratado à parte depois
      const dir = path.join(MODULOS, pasta);
      const arquivos = fs.readdirSync(dir).filter((f) => f.endsWith('.md') || f.endsWith('.ipynb'));

      const unidades = [];
      for (const arq of arquivos) {
        const base = arq.replace(/\.(md|ipynb)$/, '');
        const tipo = tipoDe(base);
        const isLab = arq.endsWith('.ipynb');
        if (isLab) {
          unidades.push({ tipo: 'lab', base, titulo: 'Lab — ' + base.replace(/^lab-\d+-/, '').replace(/-/g, ' '), isLab: true, href: `/lite/lab/index.html?path=${arq}` });
          continue;
        }
        const raw = fs.readFileSync(path.join(dir, arq), 'utf8');
        const titulo = tituloDe(raw, base);
        const corpo = preprocessMyst(raw);
        const slug = `${pasta}/${base}`;
        const fm = [
          '---',
          `title: ${JSON.stringify(titulo)}`,
          `modulo: ${JSON.stringify(pasta)}`,
          `moduloNome: ${JSON.stringify(mod.nome)}`,
          `moduloId: ${JSON.stringify(mod.id)}`,
          `eixo: ${eixo.id}`,
          `tipo: ${JSON.stringify(tipo)}`,
          '---',
          '',
        ].join('\n');
        const destDir = path.join(OUT_CONTENT, pasta);
        mkdirp(destDir);
        fs.writeFileSync(path.join(destDir, base + '.md'), fm + corpo, 'utf8');
        unidades.push({ tipo, base, titulo, isLab: false, slug });
      }

      unidades.sort((a, b) => (ORDEM[a.tipo] - ORDEM[b.tipo]) || a.base.localeCompare(b.base));
      modsOut.push({ id: mod.id, nome: mod.nome, ch: mod.ch, pasta, unidades });
    }
    eixosOut.push({ id: eixo.id, nome: eixo.nome, modulos: modsOut });
  }

  fs.writeFileSync(path.join(OUT_DATA, 'curso.json'), JSON.stringify({ eixos: eixosOut }, null, 2), 'utf8');

  const nMods = eixosOut.reduce((n, e) => n + e.modulos.length, 0);
  const nUnid = eixosOut.reduce((n, e) => n + e.modulos.reduce((m, mod) => m + mod.unidades.length, 0), 0);
  console.log(`sync ok: ${eixosOut.length} eixos, ${nMods} módulos, ${nUnid} unidades.`);
}

main();
