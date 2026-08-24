import Link from 'next/link';
import curso from '../../src/data/curso.json';

export const metadata = { title: 'Trilha — Engenharia de Dados' };

export default function Trilha() {
  const total = curso.eixos.reduce((n, e) => n + e.modulos.length, 0);
  return (
    <main className="wrap" style={{ paddingTop: 32, paddingBottom: 48 }}>
      <h1 style={{ fontSize: 30 }}>Trilha da Especialização</h1>
      <p className="muted" style={{ fontSize: 16, margin: '8px 0 0' }}>{total} disciplinas · {curso.eixos.length} eixos — avance por maestria, um módulo por vez.</p>

      <div style={{ marginTop: 24, display: 'flex', flexDirection: 'column', gap: 26 }}>
        {curso.eixos.map((eixo) => (
          <section key={eixo.id}>
            <div style={{ fontFamily: 'var(--sora)', fontWeight: 600, fontSize: 13, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '.05em', marginBottom: 10 }}>Eixo {eixo.id} — {eixo.nome}</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {eixo.modulos.map((mod) => {
                const temTeoria = mod.unidades.some((u) => u.tipo === 'teoria');
                return (
                  <Link key={mod.pasta} href={`/modulo/${mod.pasta}`} className="card card-link" style={{ padding: '14px 18px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'var(--ink)', gap: 12 }}>
                    <div>
                      <div style={{ fontFamily: 'var(--sora)', fontWeight: 600, fontSize: 16 }}>{mod.id} · {mod.nome}</div>
                      <div className="muted" style={{ fontSize: 13 }}>{mod.ch}h · {mod.unidades.length} unidades</div>
                    </div>
                    <span className="pill" style={temTeoria ? undefined : { background: 'var(--border)', color: 'var(--muted)' }}>{temTeoria ? 'Disponível' : 'Em breve'}</span>
                  </Link>
                );
              })}
            </div>
          </section>
        ))}
      </div>
    </main>
  );
}
