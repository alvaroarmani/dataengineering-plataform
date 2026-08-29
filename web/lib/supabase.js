'use client';
import { createClient } from '@supabase/supabase-js';

// A anon key é PÚBLICA por design (protegida por RLS). Configure em .env.local / Vercel:
//   NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY
const URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const ANON = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

// Sem credenciais, o app roda em modo "deslogado" (progresso em localStorage).
export const supabase = URL && ANON ? createClient(URL, ANON) : null;
export const supabaseHabilitado = Boolean(supabase);
