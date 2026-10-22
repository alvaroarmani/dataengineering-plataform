'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import curso from '../../src/data/curso.json';
import { usePlataforma } from '../../components/Plataforma.jsx';
import TrilhaPipeline from '../../components/TrilhaPipeline.jsx';
import { pctEixo, pctTotal, totais, concluidasNoModulo, proximaAula } from '../../lib/progressoCalc.js';

const N = ({ children, cor }) => <strong style={{ color: cor || 'var(--green-d)', fontVariantNumeric: 'tabular-nums' }}>{children}</strong>;

export default function Painel() {
  const { concluidas = new Set(), streak = 0, usuario } = usePlataforma() || {};
  const [hoje, setHoje] = useState('');
  useEffect(() => {
    const d = new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' });
    setHoje(d.charAt(0).toUpperCase() + d.slice(1));
  }, []);

  const total = totais(curso);
  const pct = pctTotal(concluidas, curso);
  const modsConcluidos = curso.eixos.reduce((n, e) => n + e.modulos.filter((m) => m.unidades.length && concluidasNoModulo(concluidas, m) === m.unidades.length).length, 0);
  const totalMods = curso.eixos.reduce((n, e) => n + e.modulos.length, 0);
  const prox = proximaAula(curso, concluidas);
  const primeiroNome = (usuario?.user_metadata?.name || '').split(' ')[0];

  const conquistas = [
    { ok: concluidas.size >= 1, t: 'Primeira unidade concluída' },
    { ok: modsConcluidos >= 1, t: 'Primeiro módulo completo' },
    { ok: streak >= 7, t: 'Sete dias seguidos de estudo' },
    { ok: pctEixo(concluidas, curso.eixos[0]) === 100, t: 'Eixo 1 completo' },
  ];

  return (
    <main className="wrap" style={{ paddingTop: 40, paddingBottom: 64 }}>
      <p className="muted" style={{ fontSize: 14, margin: 0 }}>{hoje}</p>
      <h1 style={{ fontSize: 'clamp(28px,4vw,40px)', letterSpacing: '-0.025em', marginTop: 6 }}>Seu painel{primeiroNome ? `, ${primeiroNome}` : ''}</h1>

      <p className="painel-lede">
        Você concluiu <N>{concluidas.size}</N> de {total} unidades, <N>{pct}%</N> do curso,
        e <N>{modsConcluidos}</N> de {totalMods} módulos.{' '}
        {streak > 0
          ? <>Seu streak está em <N cor="var(--gold)">{streak} {streak === 1 ? 'dia' : 'dias'}</N>.</>
          : 'Conclua uma unidade hoje para começar um streak.'}
      </p>

      <section style={{ marginTop: 40 }}>
        <h2 style={{ fontSize: 20, marginBottom: 18 }}>Mapa do curso</h2>
        <TrilhaPipeline />
      </section>

      <div className="grid grid-painel" style={{ marginTop: 44, gap: 28, alignItems: 'start' }}>
        <div className="card" style={{ padding: 24, background: 'var(--green)', borderColor: 'var(--green)', color: '#fff' }}>
          <p style={{ margin: 0, fontSize: 14, fontWeight: 600, color: 'rgba(255,255,255,.85)' }}>{prox ? 'Continue de onde parou' : 'Curso concluído'}</p>
          <p style={{ fontFamily: 'var(--sora)', fontWeight: 600, fontSize: 21, lineHeight: 1.3, margin: '8px 0 4px' }}>{prox ? prox.unidade.titulo : 'Você concluiu todas as unidades disponíveis.'}</p>
          {prox && <p style={{ fontSize: 14, color: 'rgba(255,255,255,.85)', margin: '0 0 18px' }}>{prox.mod.id}, {prox.mod.nome}</p>}
          {prox && (
            <Link href={`/aula/${prox.pasta}/${prox.base}`} className="btn" style={{ background: '#fff', color: 'var(--green-d)' }}>Retomar a aula</Link>
          )}
        </div>

        <section>
          <h2 style={{ fontSize: 20, marginBottom: 12 }}>Conquistas</h2>
          <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
            {conquistas.map((c) => (
              <li key={c.t} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 0', borderBottom: '1px solid var(--border)', color: c.ok ? 'var(--ink)' : 'var(--muted)' }}>
                <span aria-hidden="true" style={{ width: 22, height: 22, borderRadius: 999, flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', background: c.ok ? 'var(--gold)' : 'transparent', border: c.ok ? 0 : '2px solid var(--border)' }}>
                  {c.ok && <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="3"><path d="M20 6 9 17l-5-5" /></svg>}
                </span>
                <span style={{ fontWeight: c.ok ? 600 : 500 }}>{c.t}</span>
                <span className="sr-only">{c.ok ? '(conquistada)' : '(ainda não)'}</span>
              </li>
            ))}
          </ul>
          {!usuario && (
            <p className="muted" style={{ fontSize: 14, marginTop: 18 }}>Seu progresso está salvo <strong>neste navegador</strong>. Entre com o Google, no topo da página, para sincronizar entre dispositivos.</p>
          )}
        </section>
      </div>
    </main>
  );
}
