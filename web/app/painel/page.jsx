'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import curso from '../../src/data/curso.json';
import { usePlataforma } from '../../components/Plataforma.jsx';
import { pctEixo, pctTotal, totais, concluidasNoModulo, proximaAula } from '../../lib/progressoCalc.js';

export default function Painel() {
  const { concluidas = new Set(), streak = 0, usuario } = usePlataforma() || {};
  const [hoje, setHoje] = useState('');
  useEffect(() => { setHoje(new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' })); }, []);

  const total = totais(curso);
  const feitas = [...concluidas].filter((id) => total).length; // = concluidas.size (todas contam)
  const pct = pctTotal(concluidas, curso);
  const modsConcluidos = curso.eixos.reduce((n, e) => n + e.modulos.filter((m) => m.unidades.length && concluidasNoModulo(concluidas, m) === m.unidades.length).length, 0);
  const totalMods = curso.eixos.reduce((n, e) => n + e.modulos.length, 0);
  const prox = proximaAula(curso, concluidas);

  const stat = (v, l, cor) => (
    <div className="card" style={{ padding: 20, textAlign: 'center' }}>
      <div style={{ fontFamily: 'var(--sora)', fontWeight: 700, fontSize: 30, color: cor || 'var(--green-d)' }}>{v}</div>
      <div className="lbl">{l}</div>
    </div>
  );

  return (
    <main className="wrap" style={{ paddingTop: 32, paddingBottom: 48 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 22, gap: 12, flexWrap: 'wrap' }}>
        <h1 style={{ fontSize: 28 }}>Seu painel{usuario ? `, ${(usuario.user_metadata?.name || '').split(' ')[0] || ''}` : ''}</h1>
        <span className="muted" style={{ fontSize: 14 }}>{hoje}</span>
      </div>

      <div className="grid grid-stats" style={{ marginBottom: 22 }}>
        {stat(streak, streak === 1 ? 'dia de streak' : 'dias de streak', 'var(--gold)')}
        {stat(pct + '%', 'progresso total')}
        {stat(`${concluidas.size}/${total}`, 'unidades concluídas')}
        {stat(`${modsConcluidos}/${totalMods}`, 'módulos concluídos')}
      </div>

      <div className="grid grid-painel">
        <div className="grid" style={{ gap: 20 }}>
          <div className="card" style={{ padding: 20 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}><h3 style={{ fontSize: 17 }}>Mapa do curso</h3><span className="muted" style={{ fontSize: 13 }}>{modsConcluidos} / {totalMods} módulos</span></div>
            <div className="grid" style={{ gap: 14 }}>
              {curso.eixos.map((e) => {
                const p = pctEixo(concluidas, e);
                return (
                  <div key={e.id}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13, marginBottom: 5 }}><span style={{ fontWeight: 600, color: p ? 'var(--ink)' : 'var(--muted)' }}>Eixo {e.id} — {e.nome}</span><span className="muted">{p}%</span></div>
                    <div className="bar" style={{ background: 'var(--border)' }}><span style={{ width: p + '%' }} /></div>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="card" style={{ padding: 20 }}>
            <h3 style={{ fontSize: 17, marginBottom: 12 }}>Conquistas</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10 }}>
              <span className="pill" style={concluidas.size >= 1 ? { background: 'var(--gold-bg)', color: 'var(--gold)' } : { background: 'var(--green-t)', color: 'var(--muted)' }}>🎯 1ª unidade</span>
              <span className="pill" style={modsConcluidos >= 1 ? { background: 'var(--gold-bg)', color: 'var(--gold)' } : { background: 'var(--green-t)', color: 'var(--muted)' }}>🥇 1º módulo</span>
              <span className="pill" style={streak >= 7 ? { background: 'var(--gold-bg)', color: 'var(--gold)' } : { background: 'var(--green-t)', color: 'var(--muted)' }}>🔥 7 dias seguidos</span>
              <span className="pill" style={pctEixo(concluidas, curso.eixos[0]) === 100 ? { background: 'var(--gold-bg)', color: 'var(--gold)' } : { background: 'var(--green-t)', color: 'var(--muted)' }}>🧱 Eixo 1 completo</span>
            </div>
          </div>
        </div>

        <div className="grid" style={{ gap: 20 }}>
          <div className="card" style={{ padding: 20, background: 'var(--green)', borderColor: 'var(--green)', color: '#fff' }}>
            <div className="lbl" style={{ color: 'rgba(255,255,255,.8)' }}>Continue de onde parou</div>
            <div style={{ fontFamily: 'var(--sora)', fontWeight: 600, fontSize: 17, margin: '8px 0 4px' }}>{prox ? prox.unidade.titulo : 'Tudo concluído! 🎉'}</div>
            <p style={{ fontSize: 13, color: 'rgba(255,255,255,.85)', margin: '0 0 14px' }}>{prox ? `${prox.mod.id} · ${prox.mod.nome}` : 'Você concluiu todas as unidades disponíveis.'}</p>
            {prox && (
              <Link href={`/aula/${prox.pasta}/${prox.base}`} style={{ display: 'block', textAlign: 'center', background: '#fff', color: 'var(--green-d)', borderRadius: 9, padding: '11px 16px', fontWeight: 700, fontFamily: 'var(--man)', minHeight: 44 }}>Retomar</Link>
            )}
          </div>
          {!usuario && (
            <div className="card" style={{ padding: 20 }}>
              <div className="lbl">Salvar seu progresso</div>
              <p style={{ fontSize: 14, margin: '10px 0 0' }}>Seu progresso está salvo <strong>neste navegador</strong>. Entre com o Google (botão no topo) para sincronizar entre dispositivos.</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
