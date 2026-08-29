# ADR 0008 — Autenticação Google + progresso por usuário (Supabase, client-side)

- **Status:** ✅ Aceito (2026-08-29)
- **Relacionados:** [ADR 0006 (Next/Vercel)](0006-nextjs-vercel.md)

## Contexto

O progresso vivia só em `localStorage` (por navegador, não por pessoa, sem sincronizar). O
usuário quer uma **plataforma de estudos real**: login Google (SSO) e status do curso por
usuário, entre dispositivos.

## Decisão

**Supabase** (tudo-em-um: auth Google + Postgres + RLS), integrado **client-side sobre o site
estático** — mantém SSG na Vercel, **sem backend novo**:

- `@supabase/supabase-js` no navegador cuida do OAuth Google e da sessão.
- Progresso lido/escrito direto no Postgres do Supabase, protegido por **RLS**
  (`auth.uid() = user_id`) — cada usuário só acessa o próprio.
- **Login opcional:** sem credenciais configuradas, o app roda deslogado (localStorage) e o
  site segue 100% navegável. Ao logar, o progresso local é **migrado** para a conta.
- Sincroniza **progresso (unidades concluídas) + streak**; diário e flashcards seguem locais.

## Consequências

- **Prós:** experiência de plataforma real (login, progresso entre dispositivos, "marcar
  concluída", % por módulo/eixo); mantém hospedagem estática; degrada com elegância sem env.
- **Contras:** exige o usuário criar o projeto Supabase + OAuth client do Google e configurar
  `NEXT_PUBLIC_SUPABASE_URL`/`ANON_KEY` (a `anon key` é pública por design; o Claude não insere
  credenciais). RLS é a fronteira de segurança — precisa estar correta.
- **Arquivos:** `web/lib/{supabase,progresso*}.js`, `web/components/{Plataforma,BotaoConcluir,TocModulo,ContinuarCard,Nav}.jsx`,
  `web/app/{layout,page,painel,modulo/[slug],aula/[...slug]}`, `web/supabase/{schema.sql,README.md}`.

Setup completo: `web/supabase/README.md`.
