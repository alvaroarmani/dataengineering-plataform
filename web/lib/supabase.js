'use client';
import { createClient } from '@supabase/supabase-js';

// A anon key é PÚBLICA por design (protegida por RLS). Configure em .env.local / Vercel:
//   NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY
const URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const ANON = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

// Site estático (SPA): fluxo implicit + detecção do token no hash da URL do callback.
export const supabase = URL && ANON
  ? createClient(URL, ANON, {
      auth: {
        flowType: 'implicit',
        detectSessionInUrl: true,
        persistSession: true,
        autoRefreshToken: true,
      },
    })
  : null;
export const supabaseHabilitado = Boolean(supabase);
