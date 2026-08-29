'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import { usePlataforma } from './Plataforma.jsx';

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

function Avatar({ usuario }) {
  const foto = usuario?.user_metadata?.avatar_url;
  const nome = usuario?.user_metadata?.name || usuario?.email || 'Você';
  if (foto) return <img className="avatar" src={foto} alt={nome} referrerPolicy="no-referrer" style={{ objectFit: 'cover' }} />;
  return <div className="avatar">{(nome[0] || 'V').toUpperCase()}</div>;
}

export default function Nav() {
  const path = usePathname() || '/';
  const [aberto, setAberto] = useState(false);
  const plat = usePlataforma() || {};
  const { streak = 0, usuario = null, entrar, sair, authHabilitado } = plat;
  const cls = (href) => ((href === '/' ? path === '/' : path.startsWith(href)) ? 'active' : '');

  useEffect(() => { setAberto(false); }, [path]);

  return (
    <>
      <nav className="nav">
        <div style={{ display: 'flex', alignItems: 'center', gap: 32 }}>
          <Link href="/" style={{ display: 'flex', alignItems: 'center', gap: 10, color: 'var(--ink)' }}>
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="var(--green)" strokeWidth="2.2"><circle cx="6" cy="6" r="3" /><circle cx="6" cy="18" r="3" /><circle cx="18" cy="12" r="3" /><path d="M8.5 7.5 15 11M8.5 16.5 15 13" /></svg>
            <span style={{ fontFamily: 'var(--sora)', fontWeight: 700, fontSize: 17 }}>Eng. de Dados</span>
          </Link>
          <div className="nav-links">
            {LINKS.map((l) => (<Link key={l.href} href={l.href} className={cls(l.href)}>{l.rotulo}</Link>))}
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          {streak > 0 && (
            <span className="pill hide-sm"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" strokeWidth="2"><path d="M12 3c1 3 4 4 4 8a4 4 0 1 1-8 0c0-2 1-3 2-4" /></svg>{streak} {streak === 1 ? 'dia' : 'dias'}</span>
          )}
          <button className="icon-btn" onClick={alternarTema} aria-label="Alternar tema">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" /></svg>
          </button>
          {/* Auth: entrar (deslogado) / avatar + sair (logado). Sem Supabase configurado, some. */}
          {usuario ? (
            <>
              <Avatar usuario={usuario} />
              <button className="btn btn-s hide-sm" onClick={sair} style={{ minHeight: 38, padding: '8px 12px', fontSize: 14 }}>Sair</button>
            </>
          ) : authHabilitado ? (
            <button className="btn btn-p hide-sm" onClick={entrar} style={{ minHeight: 38, padding: '8px 14px', fontSize: 14 }}>Entrar com Google</button>
          ) : null}
          <button className="nav-burger" onClick={() => setAberto((v) => !v)} aria-label={aberto ? 'Fechar menu' : 'Abrir menu'} aria-expanded={aberto}>
            {aberto
              ? <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 6l12 12M18 6L6 18" /></svg>
              : <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 7h16M4 12h16M4 17h16" /></svg>}
          </button>
        </div>
      </nav>
      {aberto && (
        <div className="nav-sheet" role="menu">
          {LINKS.map((l) => (<Link key={l.href} href={l.href} className={cls(l.href)} role="menuitem">{l.rotulo}</Link>))}
          {usuario ? (
            <a role="menuitem" onClick={() => { setAberto(false); sair && sair(); }} style={{ cursor: 'pointer' }}>Sair ({usuario.user_metadata?.name || usuario.email})</a>
          ) : authHabilitado ? (
            <a role="menuitem" onClick={() => { setAberto(false); entrar && entrar(); }} style={{ cursor: 'pointer' }}>Entrar com Google</a>
          ) : null}
        </div>
      )}
    </>
  );
}
