'use client';
import { usePlataforma } from './Plataforma.jsx';

export default function BotaoConcluir({ aulaId }) {
  const plat = usePlataforma();
  if (!plat || !plat.pronto) return null;
  const feita = plat.estaConcluida(aulaId);
  return (
    <div style={{ display: 'flex', justifyContent: 'center', gap: 10, padding: '10px 16px', borderTop: '1px solid var(--border)', flexWrap: 'wrap', alignItems: 'center' }}>
      <button
        className={feita ? 'btn btn-s' : 'btn btn-p'}
        onClick={() => plat.alternarConcluida(aulaId)}
        style={feita ? { borderColor: 'var(--green)', color: 'var(--green-d)' } : undefined}
      >
        {feita ? (
          <><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4"><path d="M20 6 9 17l-5-5" /></svg> Concluída</>
        ) : ('Marcar como concluída')}
      </button>
      {!plat.usuario && plat.authHabilitado && (
        <span className="muted" style={{ fontSize: 12.5 }}>Entre com Google para salvar seu progresso entre dispositivos.</span>
      )}
    </div>
  );
}
