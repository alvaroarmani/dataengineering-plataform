# Login Google + progresso por usuário (Supabase) — setup

O site funciona **sem** isto (progresso fica no `localStorage`). Configure para ativar o
**login com Google** e **sincronizar o progresso entre dispositivos**.

> Segurança: a `anon key` do Supabase é **pública por design** (protegida por RLS) e vai em
> `NEXT_PUBLIC_*`. Ninguém precisa da sua senha; o Claude não insere suas credenciais.

## 1. Criar o projeto Supabase
1. Em <https://supabase.com>, crie um projeto (free tier).
2. Em **Project Settings → API**, copie **Project URL** e a **anon public key**.

## 2. Ativar o login Google
1. No Google Cloud Console, crie um **OAuth 2.0 Client ID** (tipo *Web*). Em *Authorized
   redirect URIs*, adicione o callback do Supabase: `https://<SEU-PROJETO>.supabase.co/auth/v1/callback`.
2. No Supabase → **Authentication → Providers → Google**: cole o *Client ID* e *Client Secret* e ative.
3. Em **Authentication → URL Configuration**, adicione a URL do site (produção e
   `http://localhost:3000`) em *Site URL* / *Redirect URLs*.

## 3. Criar as tabelas (RLS)
No **SQL Editor** do Supabase, rode o conteúdo de [`schema.sql`](schema.sql).

## 4. Variáveis de ambiente
Crie `web/.env.local` (não versionar) e configure o mesmo na **Vercel** (Project → Settings →
Environment Variables):
```
NEXT_PUBLIC_SUPABASE_URL=https://<SEU-PROJETO>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<sua-anon-key>
```
Rode `npm run dev` (local) ou faça redeploy na Vercel. O botão **"Entrar com Google"** aparece
no topo; ao logar, seu progresso local é **migrado** para a conta e passa a sincronizar.

## Como funciona
- Sem env → modo deslogado (localStorage), site 100% navegável.
- Com env + login → progresso em `progresso_usuario` (RLS: cada um só vê o seu) e streak em
  `perfil_usuario`. Ver [`ADR 0008`](../../docs/decisoes/0008-auth-progresso-supabase.md).
