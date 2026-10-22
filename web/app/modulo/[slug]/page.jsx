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

  return (
    <main className="wrap" style={{ paddingTop: 32, paddingBottom: 64 }}>
      <nav className="muted" style={{ fontSize: 13.5 }} aria-label="Você está em">
        <Link href="/trilha" style={{ color: 'var(--muted)' }}>Trilha</Link>
        <span aria-hidden="true"> / </span>
        <Link href={`/trilha#eixo-${eixo.id}`} style={{ color: 'var(--muted)' }}>Eixo {eixo.id}, {eixo.nome}</Link>
      </nav>
      <header style={{ margin: '12px 0 32px', maxWidth: 760 }}>
        <span className="codigo" style={{ fontSize: 14 }}>{mod.id}</span>
        <h1 style={{ fontSize: 'clamp(28px,4vw,40px)', letterSpacing: '-0.025em', marginTop: 4 }}>{mod.nome}</h1>
        <p className="muted" style={{ fontSize: 15, margin: '10px 0 0' }}>{mod.ch} horas de estudo em {mod.unidades.length} unidades.</p>
      </header>

      <div className="grid grid-modulo" style={{ gap: 48 }}>
        {/* a ementa (index.md) abre com o próprio título do módulo; o cabeçalho acima já o mostra */}
        <div className="prosa ementa" dangerouslySetInnerHTML={{ __html: mod.indexHtml || '<p class="muted">Ementa em preparação.</p>' }} />
        <TocModulo pasta={mod.pasta} unidades={mod.unidades.map(({ base, titulo, tipo }) => ({ base, titulo, tipo }))} />
      </div>
    </main>
  );
}
