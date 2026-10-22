import Link from 'next/link';
import curso from '../src/data/curso.json';
import ContinuarCard from '../components/ContinuarCard.jsx';
import TrilhaPipeline from '../components/TrilhaPipeline.jsx';

const modulos = curso.eixos.flatMap((e) => e.modulos);
const horas = modulos.reduce((n, m) => n + (m.ch || 0), 0);

export default function Home() {
  return (
    <main className="wrap" style={{ paddingTop: 48, paddingBottom: 56 }}>
      <section className="grid grid-hero">
        <div>
          <p className="muted" style={{ fontSize: 15, fontWeight: 600, margin: 0 }}>Programa autodirigido de {modulos.length} disciplinas e {horas} horas</p>
          <h1 className="hero-h1">Vire Engenheiro de Dados, de verdade.</h1>
          <p style={{ fontSize: 18, color: 'var(--muted)', maxWidth: 520, margin: '0 0 26px' }}>Teoria com o porquê, notebooks que rodam no navegador e exercícios que se corrigem sozinhos. Você sai com competência real e um portfólio no GitHub.</p>
          <Link className="btn btn-s" href="/trilha">Ver a trilha completa</Link>
        </div>

        <ContinuarCard />
      </section>

      <section style={{ marginTop: 56 }}>
        <h2 style={{ fontSize: 22, marginBottom: 6 }}>Sua trilha, do dado bruto ao Data Warehouse</h2>
        <p className="muted" style={{ fontSize: 15, margin: '0 0 22px', maxWidth: 640 }}>Cada eixo constrói uma peça do pipeline que você entrega no TCC. O duto enche conforme você conclui as unidades.</p>
        <TrilhaPipeline />
      </section>

      <section style={{ marginTop: 40 }}>
        <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start', background: 'var(--gold-bg)', border: '1px solid var(--border)', borderRadius: 12, padding: '16px 18px' }}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" strokeWidth="2" style={{ flexShrink: 0, marginTop: 2 }}><circle cx="12" cy="12" r="9" /><path d="M12 8v5M12 16h.01" /></svg>
          <p style={{ margin: 0, fontSize: 14, color: 'var(--ink)' }}><strong>Franqueza:</strong> este não é um diploma reconhecido pelo MEC nem um curso credenciado. O valor está na competência real que você desenvolve e no portfólio que constrói.</p>
        </div>
      </section>
    </main>
  );
}
