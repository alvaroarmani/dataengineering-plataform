import Link from 'next/link';
import curso from '../../../src/data/curso.json';

export function generateStaticParams() {
  const out = [];
  for (const e of curso.eixos) for (const m of e.modulos) out.push({ slug: m.pasta });
  return out;
}

function achar(slug) {
  for (const e of curso.eixos) for (const m of e.modulos) if (m.pasta === slug) return { mod: m, eixo: e };
  return {};
}

const ICON = {
  teoria: 'M4 19V5a1 1 0 0 1 1-1h11l4 4v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z',
  lab: 'M4 4h16v12H4zM8 20h8M12 16v4',
  exercicio: 'M7 4l12 8-12 8z',
  flashcards: 'M6 4h12v16l-6-3-6 3z',
  recursos: 'M4 5h16M4 12h16M4 19h10',
};
const ROTULO = { teoria: 'Teoria', lab: 'Lab', exercicio: 'Exercício', flashcards: 'Flashcards', recursos: 'Recursos' };

export default function Modulo({ params }) {
  const { mod, eixo } = achar(params.slug);
  if (!mod) return <main className="wrap" style={{ padding: 40 }}>Módulo não encontrado.</main>;
  const primeira = mod.unidades[0];

  return (
    <main className="wrap" style={{ paddingTop: 28, paddingBottom: 48 }}>
      <div className="muted" style={{ fontSize: 13 }}><Link href="/trilha" style={{ color: 'var(--muted)' }}>Trilha</Link> / Eixo {eixo.id} — {eixo.nome}</div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', gap: 20, margin: '10px 0 24px', flexWrap: 'wrap' }}>
        <div>
          <h1 style={{ fontSize: 30, maxWidth: 640 }}>{mod.id} — {mod.nome}</h1>
          <div className="muted" style={{ fontSize: 14, marginTop: 8 }}>{mod.ch} horas · {mod.unidades.length} unidades</div>
        </div>
        {primeira && (
          <Link className="btn btn-p" href={`/aula/${mod.pasta}/${primeira.base}`}>Começar módulo
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M9 6l6 6-6 6" /></svg>
          </Link>
        )}
      </div>

      <div className="grid" style={{ gridTemplateColumns: '1fr 320px', gap: 28, alignItems: 'start' }}>
        <div className="prosa" dangerouslySetInnerHTML={{ __html: mod.indexHtml || '<p class="muted">Ementa em preparação.</p>' }} />

        <aside className="card" style={{ padding: 8, position: 'sticky', top: 90 }}>
          <div className="lbl" style={{ padding: '12px 12px 6px' }}>Conteúdo do módulo</div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {mod.unidades.map((u) => (
              <Link key={u.base} href={`/aula/${mod.pasta}/${u.base}`} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '11px 12px', borderRadius: 10, color: 'var(--ink)' }}>
                <span style={{ width: 28, height: 28, borderRadius: 8, background: 'var(--green-t)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green-d)" strokeWidth="2"><path d={ICON[u.tipo] || ICON.recursos} /></svg>
                </span>
                <span style={{ minWidth: 0 }}>
                  <span style={{ display: 'block', fontWeight: 600, fontSize: 14, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{u.titulo}</span>
                  <span className="muted" style={{ fontSize: 12 }}>{ROTULO[u.tipo] || u.tipo}</span>
                </span>
              </Link>
            ))}
          </div>
        </aside>
      </div>
    </main>
  );
}
