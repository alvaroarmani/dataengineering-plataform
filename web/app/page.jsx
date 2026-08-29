import Link from 'next/link';
import ContinuarCard from '../components/ContinuarCard.jsx';

const PRIMEIRA_AULA = '/aula/01-fundamentos-eng-dados/teoria-01-o-que-e-engenharia-de-dados';

const eixos = [
  { n: 'Eixo 1 — Fundamentos', d: 'Eng. de Dados, Linux/Git, Python, SQL · 155h', pct: 12, status: 'Em andamento', on: true },
  { n: 'Eixo 2 — Data Warehousing', d: 'Kimball, BigQuery, dbt · 110h', pct: 0, status: 'Bloqueado', on: false },
  { n: 'Eixo 3 — Pipelines', d: 'Ingestão, Airflow, Docker · 95h', pct: 0, status: 'Bloqueado', on: false },
  { n: 'Eixo 4 — Escala & Governança', d: 'Spark, DataOps, LGPD · 110h', pct: 0, status: 'Bloqueado', on: false },
  { n: 'Eixo 5 — Carreira & TCC', d: 'Portfólio, entrevistas, DW · 80h', pct: 0, status: 'Bloqueado', on: false },
];

const ico = (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--green-d)" strokeWidth="2"><path d="M4 7l8-4 8 4-8 4-8-4z" /><path d="M4 12l8 4 8-4M4 17l8 4 8-4" /></svg>
);

export default function Home() {
  return (
    <main className="wrap" style={{ paddingTop: 40, paddingBottom: 48 }}>
      <section className="grid grid-hero">
        <div>
          <span className="pill" style={{ background: 'var(--card)', border: '1px solid var(--border)', color: 'var(--muted)' }}>Programa autodirigido · ~550h · 16 disciplinas</span>
          <h1 style={{ fontSize: 'clamp(32px,5vw,46px)', lineHeight: 1.08, margin: '18px 0 14px' }}>Vire Engenheiro<br />de Dados, de verdade.</h1>
          <p style={{ fontSize: 18, color: 'var(--muted)', maxWidth: 520, margin: '0 0 26px' }}>Teoria com o <em>porquê</em>, notebooks que rodam no navegador e projetos reais no seu GitHub — no padrão de uma pós, focado em te deixar pronto para o mercado.</p>
          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
            <Link className="btn btn-p" href={PRIMEIRA_AULA}>Continuar de onde parei
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14M13 6l6 6-6 6" /></svg>
            </Link>
            <Link className="btn btn-s" href="/trilha">Ver a trilha completa</Link>
          </div>
        </div>

        <ContinuarCard />
      </section>

      <section style={{ marginTop: 44 }}>
        <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 16 }}>
          <h2 style={{ fontSize: 22 }}>Sua trilha em 5 eixos</h2>
          <Link href="/trilha" className="muted" style={{ fontSize: 14 }}>ver tudo →</Link>
        </div>
        <div className="grid grid-3">
          {eixos.map((e) => (
            <div key={e.n} className="card" style={{ padding: 20, opacity: e.on ? 1 : 0.82 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ width: 40, height: 40, borderRadius: 10, background: 'var(--green-t)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{ico}</div>
                <span className="pill" style={e.on ? { background: 'var(--gold-bg)', color: 'var(--gold)' } : { background: 'var(--green-t)', color: 'var(--muted)' }}>{e.status}</span>
              </div>
              <h3 style={{ fontSize: 18, margin: '14px 0 4px' }}>{e.n}</h3>
              <p className="muted" style={{ fontSize: 14, margin: '0 0 14px' }}>{e.d}</p>
              <div className="bar"><span style={{ width: e.pct + '%' }} /></div>
            </div>
          ))}
          <div className="card" style={{ padding: 20, background: 'var(--green)', borderColor: 'var(--green)', color: '#fff' }}>
            <div style={{ width: 40, height: 40, borderRadius: 10, background: 'rgba(255,255,255,.18)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2"><path d="M12 15V3M8 7l4-4 4 4" /><path d="M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4" /></svg></div>
            <h3 style={{ fontSize: 18, margin: '14px 0 4px', color: '#fff' }}>O objetivo</h3>
            <p style={{ fontSize: 14, margin: 0, color: 'rgba(255,255,255,.9)' }}>Competência real + portfólio para uma vaga Júnior/Pleno de Engenharia de Dados.</p>
          </div>
        </div>
      </section>

      <section style={{ marginTop: 28 }}>
        <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start', background: 'var(--gold-bg)', border: '1px solid var(--border)', borderRadius: 12, padding: '16px 18px' }}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" strokeWidth="2" style={{ flexShrink: 0, marginTop: 2 }}><circle cx="12" cy="12" r="9" /><path d="M12 8v5M12 16h.01" /></svg>
          <p style={{ margin: 0, fontSize: 14, color: 'var(--ink)' }}><strong>Franqueza:</strong> este não é um diploma reconhecido pelo MEC nem um curso credenciado. O valor está na competência real que você desenvolve e no portfólio que constrói.</p>
        </div>
      </section>
    </main>
  );
}
