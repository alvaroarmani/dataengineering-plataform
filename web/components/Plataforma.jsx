'use client';
import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { supabase, supabaseHabilitado } from '../lib/supabase.js';

const Ctx = createContext(null);
export const usePlataforma = () => useContext(Ctx);

const K_CONCLUIDAS = 'de_concluidas';
const K_STREAK = 'de_streak';
const K_ULTIMA = 'de_last_visit';

const ler = (k, d) => { try { const v = localStorage.getItem(k); return v === null ? d : v; } catch { return d; } };
const grav = (k, v) => { try { localStorage.setItem(k, v); } catch {} };
function localConcluidas() { try { return new Set(JSON.parse(ler(K_CONCLUIDAS, '[]'))); } catch { return new Set(); } }
function salvarLocal(set) { grav(K_CONCLUIDAS, JSON.stringify([...set])); }

function limparHash() {
  try {
    if (typeof window !== 'undefined' && /access_token|error=/.test(window.location.hash)) {
      window.history.replaceState(null, '', window.location.pathname + window.location.search);
    }
  } catch {}
}

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

  const carregarLocal = useCallback(() => {
    setConcluidas(localConcluidas());
    const { streak: s, dia, mudou } = calcStreak(ler(K_ULTIMA, ''), parseInt(ler(K_STREAK, '0'), 10) || 0);
    if (mudou) { grav(K_STREAK, String(s)); grav(K_ULTIMA, dia); }
    setStreak(s);
  }, []);

  // Carrega do servidor; NUNCA lança (se as tabelas/RLS falharem, cai no local e segue).
  const carregarServidor = useCallback(async (user) => {
    setUsuario(user);
    try {
      const { data, error } = await supabase.from('progresso_usuario').select('aula_id');
      if (error) throw error;
      const serverSet = new Set((data || []).map((r) => r.aula_id));
      const local = localConcluidas();
      if (serverSet.size === 0 && local.size > 0) {
        await supabase.from('progresso_usuario').upsert([...local].map((aula_id) => ({ user_id: user.id, aula_id })));
        local.forEach((a) => serverSet.add(a));
      }
      setConcluidas(serverSet);
      const { data: perfil } = await supabase.from('perfil_usuario').select('*').eq('user_id', user.id).maybeSingle();
      const { streak: s, dia, mudou } = calcStreak(perfil?.ultima_visita || '', perfil?.streak || 0);
      if (mudou || !perfil) await supabase.from('perfil_usuario').upsert({ user_id: user.id, streak: s, ultima_visita: dia, atualizado_em: new Date().toISOString() });
      setStreak(s);
    } catch (e) {
      console.warn('[plataforma] progresso no servidor indisponível, usando local:', e?.message || e);
      carregarLocal();
    }
  }, [carregarLocal]);

  useEffect(() => {
    let vivo = true;
    (async () => {
      try {
        if (supabaseHabilitado) {
          const { data: { session } } = await supabase.auth.getSession();
          limparHash();
          if (!vivo) return;
          if (session?.user) await carregarServidor(session.user); else carregarLocal();
          supabase.auth.onAuthStateChange(async (_e, sess) => {
            limparHash();
            if (sess?.user) await carregarServidor(sess.user);
            else { setUsuario(null); carregarLocal(); }
          });
        } else {
          carregarLocal();
        }
      } catch (e) {
        console.warn('[plataforma] init falhou, usando local:', e?.message || e);
        carregarLocal();
      } finally {
        if (vivo) setPronto(true);
      }
    })();
    return () => { vivo = false; };
  }, [carregarServidor, carregarLocal]);

  const alternarConcluida = useCallback(async (aulaId) => {
    setConcluidas((prev) => {
      const next = new Set(prev);
      const estava = next.has(aulaId);
      if (estava) next.delete(aulaId); else next.add(aulaId);
      if (usuario && supabaseHabilitado) {
        (estava
          ? supabase.from('progresso_usuario').delete().match({ user_id: usuario.id, aula_id: aulaId })
          : supabase.from('progresso_usuario').upsert({ user_id: usuario.id, aula_id: aulaId })
        ).then?.(({ error } = {}) => { if (error) console.warn('[plataforma] salvar progresso:', error.message); });
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
