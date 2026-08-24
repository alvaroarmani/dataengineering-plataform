'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

function alternarTema() {
  const el = document.documentElement;
  const atual = el.getAttribute('data-theme');
  let novo = atual === 'dark' ? 'light' : 'dark';
  if (!atual) novo = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'light' : 'dark';
  el.setAttribute('data-theme', novo);
  try { localStorage.setItem('tema', novo); } catch (e) {}
}

const LINKS = [
  { href: '/', rotulo: 'Início' },
  { href: '/trilha', rotulo: 'Trilha' },
  { href: '/painel', rotulo: 'Painel' },
  { href: '/diario', rotulo: 'Diário' },
];

export default function Nav() {
  const path = usePathname() || '/';
  const [aberto, setAberto] = useState(false);
  const [streak, setStreak] = useState(null);
  const cls = (href) => ((href === '/' ? path === '/' : path.startsWith(href)) ? 'active' : '');

  // Fecha o menu ao trocar de rota
  useEffect(() => { setAberto(false); }, [path]);
  // Streak real (mesma chave do painel)
  useEffect(() => {
    try { const s = parseInt(localStorage.getItem('de_streak') || '0', 10); if (s > 0) setStreak(s); } catch {}
  }, [path]);

  return (
    <>
      <nav className="nav">
        <div style={{ display: 'flex', alignItems: 'center', gap: 32 }}>
          <Link href="/" style={{ display: 'flex', alignItems: 'center', gap: 10, color: 'var(--ink)' }}>
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="var(--green)" strokeWidth="2.2"><circle cx="6" cy="6" r="3" /><circle cx="6" cy="18" r="3" /><circle cx="18" cy="12" r="3" /><path d="M8.5 7.5 15 11M8.5 16.5 15 13" /></svg>
            <span style={{ fontFamily: 'var(--sora)', fontWeight: 700, fontSize: 17 }}>Eng. de Dados</span>
          </Link>
          <div className="nav-links">
            {LINKS.map((l) => (
              <Link key={l.href} href={l.href} className={cls(l.href)}>{l.rotulo}</Link>
            ))}
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          {streak != null && (
            <span className="pill hide-sm"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" strokeWidth="2"><path d="M12 3c1 3 4 4 4 8a4 4 0 1 1-8 0c0-2 1-3 2-4" /></svg>{streak} {streak === 1 ? 'dia' : 'dias'}</span>
          )}
          <button className="icon-btn" onClick={alternarTema} aria-label="Alternar tema">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" /></svg>
          </button>
          <div className="avatar">A</div>
          <button
            className="nav-burger"
            onClick={() => setAberto((v) => !v)}
            aria-label={aberto ? 'Fechar menu' : 'Abrir menu'}
            aria-expanded={aberto}
          >
            {aberto ? (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 6l12 12M18 6L6 18" /></svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 7h16M4 12h16M4 17h16" /></svg>
            )}
          </button>
        </div>
      </nav>
      {aberto && (
        <div className="nav-sheet" role="menu">
          {LINKS.map((l) => (
            <Link key={l.href} href={l.href} className={cls(l.href)} role="menuitem">{l.rotulo}</Link>
          ))}
        </div>
      )}
    </>
  );
}
