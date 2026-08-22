# Flashcards — Módulo 02

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** Por que automatizar pelo terminal vs. clicar? / **R:** Comandos são salváveis, versionáveis e reexecutáveis → reprodutíveis e automatizáveis; cliques não deixam rastro nem se repetem.
- **P:** O que faz o pipe `|`? / **R:** Liga a saída (stdout) de um comando à entrada (stdin) do próximo — encadeia programas pequenos (filosofia Unix).
- **P:** Fluxo mínimo do Git? / **R:** `git add` (seleciona) → `git commit` (grava snapshot com mensagem) → `git push` (envia ao remoto).
- **P:** O que é uma branch e para que serve? / **R:** Uma linha de trabalho isolada; permite desenvolver em paralelo sem afetar a `main` e depois `merge` de volta.
- **P:** Commit é diff ou snapshot? / **R:** Snapshot — registra o estado completo do projeto, o que torna branch/merge baratos (Pro Git).
- **P:** Imagem vs container vs volume (Docker)? / **R:** Imagem = molde imutável; container = instância em execução; volume = armazenamento que persiste fora do container.
- **P:** Por que Docker num pipeline de dados? / **R:** Reprodutibilidade — mesmo ambiente em dev/CI/prod, elimina o "na minha máquina funciona".
- **P:** O que NUNCA versionar? / **R:** Segredos (`.env`, chaves) e dados grandes — use `.gitignore`.
- **P:** Três tipos de padrão de `.gitignore`? / **R:** Nome exato (`.env`), curinga de extensão (`*.log`) e pasta/prefixo (`data/`).

---
**Revisado em:** 2026-08-21
