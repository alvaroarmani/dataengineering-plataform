import Link from 'next/link';
import curso from '../../../src/data/curso.json';
import Flashcards from '../../../components/Flashcards.jsx';
import Mermaid from '../../../components/Mermaid.jsx';

export function generateStaticParams() {
  const out = [];
  for (const e of curso.eixos)
    for (const m of e.modulos)
      for (const u of m.unidades) out.push({ slug: [m.pasta, u.base] });
  return out;
}

function achar(slug) {
  const [pasta, base] = slug;
  for (const e of curso.eixos)
    for (const m of e.modulos)
      if (m.pasta === pasta) {
        const idx = m.unidades.findIndex((u) => u.base === base);
        if (idx >= 0) return { mod: m, eixo: e, u: m.unidades[idx], prev: m.unidades[idx - 1], next: m.unidades[idx + 1], pos: idx + 1, total: m.unidades.length };
      }
  return {};
}

const ROTULO = { teoria: 'Teoria', lab: 'Lab', exercicio: 'Exercício', flashcards: 'Flashcards', recursos: 'Recursos' };

export default function Aula({ params }) {
  const { mod, eixo, u, prev, next, pos, total } = achar(params.slug);
  if (!u) return <main className="wrap" style={{ padding: 40 }}>Aula não encontrada.</main>;
  const pct = Math.round((pos / total) * 100);
  const ehFlash = u.tipo === 'flashcards' && u.cards && u.cards.length;

  return (
    <div className="lesson">
      <div className="lesson-top">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, minWidth: 0 }}>
          <Link href={`/modulo/${mod.pasta}`} className="icon-btn" style={{ width: 34, height: 34 }} aria-label="Voltar ao módulo">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M15 6l-6 6 6 6" /></svg>
          </Link>
          <div className="muted" style={{ fontSize: 13, minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>Eixo {eixo.id} · {mod.id} <span style={{ opacity: .5 }}>/</span> <span style={{ color: 'var(--ink)', fontWeight: 600 }}>{ROTULO[u.tipo] || u.tipo}</span></div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 9, width: 170 }}>
          <div className="bar" style={{ flexGrow: 1, background: 'var(--border)' }}><span style={{ width: pct + '%' }} /></div>
          <span className="muted" style={{ fontSize: 12, fontWeight: 600 }}>{pos}/{total}</span>
        </div>
      </div>

      {u.isLab ? (
        <div className="lab-wrap">
          <div className="nb-toolbar">
            <div className="muted" style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13, fontWeight: 600 }}>
              <span style={{ width: 9, height: 9, borderRadius: 999, background: 'var(--green)' }} /> JupyterLite · Python (Pyodide)
            </div>
            <span className="muted" style={{ fontSize: 12 }}>roda no seu navegador</span>
          </div>
          <iframe className="nb-frame" title="Notebook interativo (JupyterLite)" src={u.href} loading="lazy" />
        </div>
      ) : ehFlash ? (
        <div className="lesson-body">
          <div className="prosa" style={{ maxWidth: 680 }}>
            <h1>🃏 Flashcards — {mod.nome}</h1>
            <p className="muted">Tente responder de memória antes de virar. Revise sempre que voltar — é assim que fixa.</p>
          </div>
          <Flashcards cards={u.cards} />
        </div>
      ) : (
        <div className="lesson-body">
          <article className="prosa" dangerouslySetInnerHTML={{ __html: u.html }} />
          <Mermaid />
        </div>
      )}

      <div className="lesson-bottom">
        {prev ? (
          <Link className="btn btn-s" href={`/aula/${mod.pasta}/${prev.base}`}><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M15 6l-6 6 6 6" /></svg><span className="hide-sm">{prev.titulo}</span><span className="only-sm">Anterior</span></Link>
        ) : (
          <Link className="btn btn-s" href={`/modulo/${mod.pasta}`}>Voltar ao módulo</Link>
        )}
        {next ? (
          <Link className="btn btn-p" href={`/aula/${mod.pasta}/${next.base}`}><span className="hide-sm">Próxima: {next.titulo}</span><span className="only-sm">Próxima</span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M9 6l6 6-6 6" /></svg></Link>
        ) : (
          <Link className="btn btn-p" href={`/modulo/${mod.pasta}`}>Concluir módulo</Link>
        )}
      </div>
    </div>
  );
}
