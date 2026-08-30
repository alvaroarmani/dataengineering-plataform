# Flashcards — Módulo 10

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** O que é uma camada e como funciona o cache? / **R:** Cada instrução do Dockerfile vira uma camada; o Docker cacheia até a 1ª que mudou — dali pra baixo, tudo rebuilda.
- **P:** Por que instalar dependências antes de `COPY . .`? / **R:** Deps mudam raramente e código sempre; assim a camada cara do pip fica em cache e mudanças de código não a invalidam.
- **P:** O que é multi-stage build? / **R:** Um estágio builder compila/instala e o final copia só o necessário — imagem enxuta, sem compiladores/caches.
- **P:** Para que serve o .dockerignore? / **R:** Excluir arquivos do contexto de build (.git, node_modules, .env) — build mais rápido, contexto menor, evita vazar segredos.
- **P:** Como um container acha outro no Compose? / **R:** Pelo nome do serviço como host (postgres:5432); localhost dentro do container é ele mesmo.
- **P:** Por que um banco precisa de volume? / **R:** O filesystem do container é efêmero; o volume persiste os dados entre reinícios/recriações.
- **P:** `ports: ["8080:80"]` significa? / **R:** Publica a porta 80 do container na 8080 do host (host:container).
- **P:** `depends_on` garante prontidão? / **R:** Não, só ordem de início; para prontidão use healthcheck.
- **P:** Por que NÃO pôr segredo na imagem? / **R:** Fica gravado nas camadas (qualquer um que puxe lê); passe em runtime (env/secrets), .env no .gitignore.
- **P:** Por que evitar `latest` em produção? / **R:** É alvo móvel; pine uma tag específica para reprodutibilidade.
- **P:** Como se lê `ghcr.io/voce/app:1.2.0`? / **R:** registry=ghcr.io, nome=voce/app, tag=1.2.0 (sem registry=docker.io, sem tag=latest).

---
**Revisado em:** 2026-08-29
