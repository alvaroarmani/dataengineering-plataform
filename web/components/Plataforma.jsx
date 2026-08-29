'use client';
import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { supabase, supabaseHabilitado } from '../lib/supabase.js';

const Ctx = createContext(null);
export const usePlataforma = () => useContext(Ctx);

const K_CONCLUIDAS = 'de_concluidas';
const K_STREAK = 'de_streak';
const K_ULTIMA = 'de_last_visit';

// ---- localStorage helpers ----
const ler = (k, d) => { try { const v = localStorage.getItem(k); return v === null ? d : v; } catch { return d; } };
const grav = (k, v) => { try { localStorage.setItem(k, v); } catch {} };
function localConcluidas() { try { return new Set(JSON.parse(ler(K_CONCLUIDAS, '[]'))); } catch { return new Set(); } }
function salvarLocal(set) { grav(K_CONCLUIDAS, JSON.stringify([...set])); }

// streak a partir de uma data ISO (yyyy-mm-dd) da última visita e do valor anterior
function calcStreak(ultima, anterior) {
  const dia = new Date().toISOString().slice(0, 10);
  if (ultima === dia) return { streak: anterior || 1, dia, mudou: false };
  let s = 1;
  if (ultima) { const diff = Math.round((new Date(dia) - new Date(ultima)) / 86400000); s = diff === 1 ? (anterior || 0) + 1 : 1; }
  return { streak: s, dia, mudou: true };
}

export default function Plataforma({ children }) {
  const [usuario, setUsuario] = useState(null);
  const [concluidas, setConcluidas] = useState(() => new Set());
  const [streak, setStreak] = useState(0);
  const [pronto, setPronto] = useState(false);

  // --- carregar do servidor (logado) ---
  const carregarServidor = useCallback(async (user) => {
    const { data } = await supabase.from('progresso_usuario').select('aula_id');
    const serverSet = new Set((data || []).map((r) => r.aula_id));
    // migração: se o servidor está vazio e há progresso local, sobe-o
    const local = localConcluidas();
    if (serverSet.size === 0 && local.size > 0) {
      const linhas = [...local].map((aula_id) => ({ user_id: user.id, aula_id }));
      await supabase.from('progresso_usuario').upsert(linhas);
      local.forEach((a) => serverSet.add(a));
    }
    setConcluidas(serverSet);
    // streak no perfil
    const { data: perfil } = await supabase.from('perfil_usuario').select('*').eq('user_id', user.id).maybeSingle();
    const { streak: s, dia, mudou } = calcStreak(perfil?.ultima_visita || '', perfil?.streak || 0);
    if (mudou || !perfil) await supabase.from('perfil_usuario').upsert({ user_id: user.id, streak: s, ultima_visita: dia, atualizado_em: new Date().toISOString() });
    setStreak(s);
  }, []);

  // --- carregar local (deslogado) ---
  const carregarLocal = useCallback(() => {
    setConcluidas(localConcluidas());
    const { streak: s, dia, mudou } = calcStreak(ler(K_ULTIMA, ''), parseInt(ler(K_STREAK, '0'), 10) || 0);
    if (mudou) { grav(K_STREAK, String(s)); grav(K_ULTIMA, dia); }
    setStreak(s);
  }, []);

  useEffect(() => {
    let vivo = true;
    (async () => {
      if (supabaseHabilitado) {
        const { data: { session } } = await supabase.auth.getSession();
        if (!vivo) return;
        if (session?.user) { setUsuario(session.user); await carregarServidor(session.user); }
        else { carregarLocal(); }
        supabase.auth.onAuthStateChange(async (_e, sess) => {
          if (sess?.user) { setUsuario(sess.user); await carregarServidor(sess.user); }
          else { setUsuario(null); carregarLocal(); }
        });
      } else {
        carregarLocal();
      }
      if (vivo) setPronto(true);
    })();
    return () => { vivo = false; };
  }, [carregarServidor, carregarLocal]);

  const alternarConcluida = useCallback(async (aulaId) => {
    setConcluidas((prev) => {
      const next = new Set(prev);
      const estava = next.has(aulaId);
      if (estava) next.delete(aulaId); else next.add(aulaId);
      // persiste
      if (usuario && supabaseHabilitado) {
        if (estava) supabase.from('progresso_usuario').delete().match({ user_id: usuario.id, aula_id: aulaId });
        else supabase.from('progresso_usuario').upsert({ user_id: usuario.id, aula_id: aulaId });
      } else {
        salvarLocal(next);
      }
      return next;
    });
  }, [usuario]);

  const estaConcluida = useCallback((aulaId) => concluidas.has(aulaId), [concluidas]);

  const entrar = useCallback(() => {
    if (!supabaseHabilitado) { alert('Login ainda não configurado (Supabase). Veja web/supabase/README.md.'); return; }
    supabase.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: window.location.origin } });
  }, []);
  const sair = useCallback(async () => { if (supabaseHabilitado) await supabase.auth.signOut(); }, []);

  const valor = { usuario, concluidas, estaConcluida, alternarConcluida, streak, pronto, entrar, sair, authHabilitado: supabaseHabilitado };
  return <Ctx.Provider value={valor}>{children}</Ctx.Provider>;
}
