'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';

const eixos = [
  { n: 'Eixo 1 — Fundamentos', pct: 12 },
  { n: 'Eixo 2 — Data Warehousing', pct: 0 },
  { n: 'Eixo 3 — Pipelines', pct: 0 },
  { n: 'Eixo 4 — Escala & Governança', pct: 0 },
];

export default function Painel() {
  const [streak, setStreak] = useState('—');
  const [north, setNorth] = useState(16);
  const [pct, setPct] = useState(6);
  const [hoje, setHoje] = useState('');

  useEffect(() => {
    setHoje(new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' }));
    const ler = (k, d) => { try { const v = localStorage.getItem(k); return v === null ? d : v; } catch { return d; } };
    const grav = (k, v) => { try { localStorage.setItem(k, v); } catch {} };
    const dia = new Date().toISOString().slice(0, 10);
    const last = ler('de_last_visit', '');
    let s = parseInt(ler('de_streak', '0'), 10) || 0;
    if (last !== dia) {
      if (last) { const diff = Math.round((new Date(dia) - new Date(last)) / 86400000); s = diff === 1 ? s + 1 : 1; }
      else s = 1;
      grav('de_streak', String(s)); grav('de_last_visit', dia);
    }
    setStreak(s);
    let done = []; try { done = JSON.parse(ler('de_modulos_concluidos', '[]')); } catch {}
    const d = Array.isArray(done) ? done.length : 0;
    setNorth(16 - d);
    if (d > 0) setPct(Math.round((d / 16) * 100));
  }, []);

  const stat = (v, l, cor) => (
    <div className="card" style={{ padding: 20, textAlign: 'center' }}>
      <div style={{ fontFamily: 'var(--sora)', fontWeight: 700, fontSize: 30, color: cor || 'var(--green-d)' }}>{v}</div>
      <div className="lbl">{l}</div>
    </div>
  );

  return (
    <main className="wrap" style={{ paddingTop: 32, paddingBottom: 48 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 22 }}>
        <h1 style={{ fontSize: 28 }}>Seu painel</h1>
        <span className="muted" style={{ fontSize: 14 }}>{hoje}</span>
      </div>

      <div className="grid grid-stats" style={{ marginBottom: 22 }}>
        {stat(streak, 'dias de streak', 'var(--gold)')}
        {stat(pct + '%', 'progresso total')}
        {stat(north, 'p/ estar pronto p/ vagas')}
        {stat(1, 'projeto no GitHub')}
      </div>

      <div className="grid grid-painel">
        <div className="grid" style={{ gap: 20 }}>
          <div className="card" style={{ padding: 20 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}><h3 style={{ fontSize: 17 }}>Mapa do curso</h3><span className="muted" style={{ fontSize: 13 }}>1 / 16 módulos</span></div>
            <div className="grid" style={{ gap: 14 }}>
              {eixos.map((e) => (
                <div key={e.n}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13, marginBottom: 5 }}><span style={{ fontWeight: 600, color: e.pct ? 'var(--ink)' : 'var(--muted)' }}>{e.n}</span><span className="muted">{e.pct}%</span></div>
                  <div className="bar" style={{ background: 'var(--border)' }}><span style={{ width: e.pct + '%' }} /></div>
                </div>
              ))}
            </div>
          </div>
          <div className="card" style={{ padding: 20 }}>
            <h3 style={{ fontSize: 17, marginBottom: 12 }}>Conquistas</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10 }}>
              <span className="pill" style={{ background: 'var(--gold-bg)', color: 'var(--gold)' }}>🥇 1º módulo</span>
              <span className="pill" style={{ background: 'var(--gold-bg)', color: 'var(--gold)' }}>✅ Testes verdes</span>
              <span className="pill" style={{ background: 'var(--green-t)', color: 'var(--muted)' }}>🔥 7 dias seguidos</span>
              <span className="pill" style={{ background: 'var(--green-t)', color: 'var(--muted)' }}>🧱 Eixo 1 completo</span>
            </div>
          </div>
        </div>

        <div className="grid" style={{ gap: 20 }}>
          <div className="card" style={{ padding: 20, background: 'var(--green)', borderColor: 'var(--green)', color: '#fff' }}>
            <div className="lbl" style={{ color: 'rgba(255,255,255,.8)' }}>Revisar hoje</div>
            <div style={{ fontFamily: 'var(--sora)', fontWeight: 600, fontSize: 18, margin: '8px 0 4px' }}>Flashcards · Módulo 1</div>
            <p style={{ fontSize: 13, color: 'rgba(255,255,255,.85)', margin: '0 0 14px' }}>Modo 5-min: mantém seu streak sem esforço.</p>
            <Link href="/aula/01-fundamentos-eng-dados/flashcards" style={{ display: 'block', textAlign: 'center', background: '#fff', color: 'var(--green-d)', borderRadius: 9, padding: '11px 16px', fontWeight: 700, fontFamily: 'var(--man)', minHeight: 44 }}>Revisar agora</Link>
          </div>
          <div className="card" style={{ padding: 20 }}>
            <div className="lbl">Desafio da semana</div>
            <p style={{ fontSize: 14, margin: '10px 0 0' }}>SQL: escreva uma query com <em>window function</em> que traga o top-3 por categoria.</p>
          </div>
        </div>
      </div>
    </main>
  );
}
