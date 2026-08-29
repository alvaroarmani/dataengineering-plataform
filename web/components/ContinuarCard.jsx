'use client';
import Link from 'next/link';
import curso from '../src/data/curso.json';
import { usePlataforma } from './Plataforma.jsx';
import { proximaAula, pctTotal } from '../lib/progressoCalc.js';

export default function ContinuarCard() {
  const { concluidas = new Set(), pronto } = usePlataforma() || {};
  const prox = proximaAula(curso, concluidas);
  const pct = pctTotal(concluidas, curso);
  const alvo = prox || { pasta: curso.eixos[0].modulos[0].pasta, base: curso.eixos[0].modulos[0].unidades[0].base, mod: curso.eixos[0].modulos[0], unidade: curso.eixos[0].modulos[0].unidades[0], eixo: curso.eixos[0] };

  return (
    <div className="card" style={{ padding: 22 }}>
      <div className="lbl">{concluidas.size > 0 ? 'Continue de onde parou' : 'Comece por aqui'}</div>
      <div style={{ display: 'flex', gap: 14, alignItems: 'center', margin: '14px 0' }}>
        <div style={{ width: 52, height: 52, borderRadius: 12, background: 'var(--green-t)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="var(--green-d)" strokeWidth="2"><path d="M4 4h16v12H4z" /><path d="M8 20h8M12 16v4" /></svg>
        </div>
        <div style={{ minWidth: 0 }}>
          <div style={{ fontFamily: 'var(--sora)', fontWeight: 600, fontSize: 16 }}>{alvo.mod.id} · {alvo.mod.nome}</div>
          <div className="muted" style={{ fontSize: 14, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{prox ? alvo.unidade.titulo : 'Tudo concluído! 🎉'}</div>
        </div>
      </div>
      <div className="bar" style={{ margin: '6px 0 8px' }}><span style={{ width: pct + '%' }} /></div>
      <div className="muted" style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13 }}><span>Progresso total</span><span>{pct}%</span></div>
      <Link className="btn btn-p" href={`/aula/${alvo.pasta}/${alvo.base}`} style={{ width: '100%', justifyContent: 'center', marginTop: 16 }}>{concluidas.size > 0 && prox ? 'Retomar' : 'Começar'}</Link>
    </div>
  );
}
