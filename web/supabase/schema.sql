-- Schema do progresso por usuário (rode no SQL Editor do seu projeto Supabase).
-- Segurança: RLS garante que cada usuário só lê/escreve as PRÓPRIAS linhas.

-- 1) Unidades concluídas (aula_id = "<pasta-do-modulo>/<base-da-unidade>")
create table if not exists public.progresso_usuario (
  user_id     uuid        not null references auth.users(id) on delete cascade,
  aula_id     text        not null,
  concluida_em timestamptz not null default now(),
  primary key (user_id, aula_id)
);

alter table public.progresso_usuario enable row level security;

drop policy if exists "progresso: dono lê" on public.progresso_usuario;
create policy "progresso: dono lê"    on public.progresso_usuario for select using (auth.uid() = user_id);
drop policy if exists "progresso: dono insere" on public.progresso_usuario;
create policy "progresso: dono insere" on public.progresso_usuario for insert with check (auth.uid() = user_id);
drop policy if exists "progresso: dono apaga" on public.progresso_usuario;
create policy "progresso: dono apaga"  on public.progresso_usuario for delete using (auth.uid() = user_id);

-- 2) Perfil / streak
create table if not exists public.perfil_usuario (
  user_id       uuid        primary key references auth.users(id) on delete cascade,
  streak        int         not null default 0,
  ultima_visita date,
  atualizado_em timestamptz not null default now()
);

alter table public.perfil_usuario enable row level security;

drop policy if exists "perfil: dono lê" on public.perfil_usuario;
create policy "perfil: dono lê"     on public.perfil_usuario for select using (auth.uid() = user_id);
drop policy if exists "perfil: dono grava" on public.perfil_usuario;
create policy "perfil: dono grava"  on public.perfil_usuario for insert with check (auth.uid() = user_id);
drop policy if exists "perfil: dono atualiza" on public.perfil_usuario;
create policy "perfil: dono atualiza" on public.perfil_usuario for update using (auth.uid() = user_id);
