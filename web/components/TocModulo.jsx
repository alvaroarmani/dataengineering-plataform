'use client';
import Link from 'next/link';
import { usePlataforma } from './Plataforma.jsx';

const ICON = {
  teoria: 'M4 19V5a1 1 0 0 1 1-1h11l4 4v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z',
  lab: 'M4 4h16v12H4zM8 20h8M12 16v4',
  exercicio: 'M7 4l12 8-12 8z',
  flashcards: 'M6 4h12v16l-6-3-6 3z',
  recursos: 'M4 5h16M4 12h16M4 19h10',
};
const ROTULO = { teoria: 'Teoria', lab: 'Lab', exercicio: 'Exercício', flashcards: 'Flashcards', recursos: 'Recursos' };

export default function TocModulo({ pasta, unidades }) {
  const plat = usePlataforma() || {};
  const feita = (base) => plat.estaConcluida ? plat.estaConcluida(`${pasta}/${base}`) : false;
  const nFeitas = unidades.filter((u) => feita(u.base)).length;
  const pct = unidades.length ? Math.round((nFeitas / unidades.length) * 100) : 0;

  return (
    <aside className="card side-toc" style={{ padding: 8, position: 'sticky', top: 90 }}>
      <div style={{ padding: '12px 12px 6px' }}>
        <div className="lbl">Conteúdo do módulo</div>
        <div className="bar" style={{ margin: '10px 0 4px', background: 'var(--border)' }}><span style={{ width: pct + '%' }} /></div>
        <div className="muted" style={{ fontSize: 12 }}>{nFeitas} de {unidades.length} concluídas · {pct}%</div>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {unidades.map((u) => {
          const ok = feita(u.base);
          return (
            <Link key={u.base} href={`/aula/${pasta}/${u.base}`} className="side-link" style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '11px 12px', borderRadius: 10, color: 'var(--ink)' }}>
              <span style={{ width: 28, height: 28, borderRadius: 8, background: ok ? 'var(--green)' : 'var(--green-t)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                {ok
                  ? <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.6"><path d="M20 6 9 17l-5-5" /></svg>
                  : <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green-d)" strokeWidth="2"><path d={ICON[u.tipo] || ICON.recursos} /></svg>}
              </span>
              <span style={{ minWidth: 0 }}>
                <span style={{ display: 'block', fontWeight: 600, fontSize: 14, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{u.titulo}</span>
                <span className="muted" style={{ fontSize: 12 }}>{ROTULO[u.tipo] || u.tipo}</span>
              </span>
            </Link>
          );
        })}
      </div>
    </aside>
  );
}
