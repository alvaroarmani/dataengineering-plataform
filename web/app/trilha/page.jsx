import curso from '../../src/data/curso.json';
import DutoModulos from '../../components/DutoModulos.jsx';

export const metadata = { title: 'Trilha — Engenharia de Dados' };

export default function Trilha() {
  const total = curso.eixos.reduce((n, e) => n + e.modulos.length, 0);
  return (
    <main className="wrap" style={{ paddingTop: 40, paddingBottom: 64, maxWidth: 860 }}>
      <h1 style={{ fontSize: 'clamp(30px,4vw,40px)', letterSpacing: '-0.025em' }}>Trilha da Especialização</h1>
      <p className="muted" style={{ fontSize: 17, margin: '10px 0 0', maxWidth: 620 }}>
        {total} disciplinas em {curso.eixos.length} eixos. Avance por maestria: conclua as unidades de um módulo e o duto enche até o próximo.
      </p>
      <p className="muted" style={{ fontSize: 13.5, margin: '8px 0 0', maxWidth: 620 }}>
        Siga a ordem de cada eixo. O código <span className="codigo">M##</span> identifica o módulo, como o código de uma disciplina; não é a posição dele na trilha.
      </p>

      <div style={{ marginTop: 36, display: 'flex', flexDirection: 'column', gap: 40 }}>
        {curso.eixos.map((eixo) => (
          <section key={eixo.id} id={`eixo-${eixo.id}`} style={{ scrollMarginTop: 90 }}>
            <h2 style={{ fontSize: 20, marginBottom: 12, paddingBottom: 10, borderBottom: '1px solid var(--border)' }}>
              <span style={{ color: 'var(--green-d)' }}>Eixo {eixo.id}.</span> {eixo.nome}
            </h2>
            <DutoModulos
              modulos={eixo.modulos.map((m) => ({
                pasta: m.pasta, id: m.id, nome: m.nome, ch: m.ch,
                bases: m.unidades.map((u) => u.base),
                disponivel: m.unidades.some((u) => u.tipo === 'teoria'),
              }))}
            />
          </section>
        ))}
      </div>
    </main>
  );
}
