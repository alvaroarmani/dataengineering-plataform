import Link from 'next/link';
import curso from '../../../src/data/curso.json';
import TocModulo from '../../../components/TocModulo.jsx';

export function generateStaticParams() {
  const out = [];
  for (const e of curso.eixos) for (const m of e.modulos) out.push({ slug: m.pasta });
  return out;
}

function achar(slug) {
  for (const e of curso.eixos) for (const m of e.modulos) if (m.pasta === slug) return { mod: m, eixo: e };
  return {};
}

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

      <div className="grid grid-modulo">
        <div className="prosa" dangerouslySetInnerHTML={{ __html: mod.indexHtml || '<p class="muted">Ementa em preparação.</p>' }} />

        <TocModulo pasta={mod.pasta} unidades={mod.unidades} />
      </div>
    </main>
  );
}
