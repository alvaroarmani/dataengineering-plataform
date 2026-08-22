# Terminal, Git e containers: seu ambiente de trabalho

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Antes de mover um byte de dado, um engenheiro precisa de um **ambiente** onde as coisas
funcionem hoje, amanhã e na máquina de outra pessoa. Três ferramentas resolvem isso e
aparecem em **toda** vaga, ainda que "escondidas" nos requisitos: o **terminal** (para
operar servidores e automatizar), o **Git** (para versionar e colaborar) e o **Docker**
(para empacotar ambientes reprodutíveis). Dominar esse tripé é o que te deixa produtivo —
e o que separa quem "roda um notebook" de quem **entrega software de dados**.

## 💡 Conceito (o porquê)

### Terminal / linha de comando
A maior parte da infraestrutura de dados roda em **Linux**, sem interface gráfica. Você
fala com ela pelo **terminal**. O ganho não é "ser hacker": é **automação** e
**repetibilidade** — um comando pode ser salvo, versionado e reexecutado, um clique não.

Ideias que pagam a conta:
- **Navegação e arquivos:** `pwd`, `ls`, `cd`, `cp`, `mv`, `rm`, `mkdir`.
- **Pipes e redirecionamento:** `|` liga a saída de um comando à entrada de outro; `>`/`>>`
  gravam em arquivo. Ex.: `cat vendas.csv | wc -l` conta as linhas. Esse encadeamento é a
  filosofia Unix — programas pequenos que fazem uma coisa bem.
- **Permissões:** `chmod`, `chown` — importam ao rodar em servidores.

### Git — versionamento
Git guarda o **histórico** do seu trabalho como uma sequência de *snapshots* (commits).
Isso te dá: desfazer com segurança, trabalhar em **branches** paralelas, colaborar sem
sobrescrever o outro, e um registro de *por que* cada mudança foi feita.

O fluxo mínimo: `git add` (seleciona o que entra) → `git commit` (grava o snapshot com uma
mensagem) → `git push` (envia para o GitHub). Branches isolam trabalho em andamento;
`merge` junta de volta.

### Docker — ambientes reprodutíveis
"Na minha máquina funciona" é o inimigo. O **Docker** empacota sua aplicação **e todas as
dependências** em uma **imagem**; dela sobem **containers** idênticos em qualquer lugar.
Três palavras:
- **Imagem:** o molde (sistema + libs + seu código), imutável.
- **Container:** uma instância em execução da imagem.
- **Volume:** armazenamento que **persiste** fora do container (senão os dados somem quando
  ele para).

É por isso que a **bancada** do curso (`ambiente/docker-compose.yml`) sobe Postgres +
JupyterLab + MinIO com um comando: o ambiente é **descrito em código** e reproduzível.

## 🔎 Exemplo

Um fluxo real de um dia de trabalho, no terminal:

```bash
git checkout -b ingestao-vendas      # nova branch
# ... edita scripts ...
git add ingest.py && git commit -m "feat: ingestão incremental de vendas"
git push -u origin ingestao-vendas   # abre PR no GitHub
docker compose up -d                 # sobe o ambiente para testar
```

Tudo isso é **versionado e reproduzível** — a base de DataOps (M13).

:::{admonition} 📖 Da literatura
:class: seealso
O *Pro Git* trata cada commit como um **snapshot** do projeto (não um "diff"), o que explica
por que criar e trocar de branch é barato e por que o histórico é confiável.
— *Pro Git*, cap. 1 e 3.
:::

## ⚠️ Erros comuns
- **Commits gigantes** e sem mensagem clara — dificultam entender e reverter. Prefira commits pequenos e descritivos.
- **Versionar segredos** (`.env`, chaves) ou **dados grandes** — use `.gitignore`.
- Confundir **imagem** (molde) com **container** (instância em execução).
- Esquecer **volumes** e perder dados ao derrubar um container.
- Editar no servidor "na unha" em vez de versionar e reimplantar.

## 💼 O que o mercado espera
Git e terminal são **pré-requisito silencioso** de qualquer vaga — ninguém lista "saber
salvar arquivo", mas todos esperam que você abra um PR e navegue num servidor. Docker
aparece explicitamente na maioria das vagas Jr/Pleno de dados.

:::{admonition} ✨ Em resumo
:class: resumo
- Terminal, Git e Docker são o **tripé** de todo engenheiro de dados.
- **Commit = snapshot**; use branch/PR para colaborar; nunca versione segredos (`.env`).
- Docker: **imagem** (molde) → **container** (execução) → **volume** (persistência).
- Automação e reprodutibilidade sempre vencem cliques manuais.
:::

## 🧠 Quiz de recall
1. Por que automatizar pelo terminal é melhor que clicar numa interface?
   :::{dropdown} Resposta
   Comandos são salváveis, versionáveis e reexecutáveis — logo reprodutíveis e automatizáveis; cliques não deixam rastro nem se repetem sozinhos.
   :::
2. Qual a diferença entre imagem, container e volume no Docker?
   :::{dropdown} Resposta
   Imagem é o molde imutável (sistema + deps + código); container é uma instância em execução da imagem; volume é armazenamento que persiste fora do container.
   :::
3. O que faz o pipe `|` no shell?
   :::{dropdown} Resposta
   Liga a saída (stdout) de um comando à entrada (stdin) do próximo, permitindo encadear programas pequenos (filosofia Unix).
   :::
4. Por que um commit no Git é descrito como um "snapshot"?
   :::{dropdown} Resposta
   Cada commit registra o estado completo do projeto naquele momento (referenciando o conteúdo), o que torna branch/merge baratos e o histórico confiável. — *Pro Git*.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você organizaria o versionamento de um projeto de dados em time?"
  :::{dropdown} Resposta modelo
  Branch por tarefa/feature, commits pequenos e descritivos, Pull Requests com revisão, `main` protegida, e CI rodando testes a cada PR. Segredos fora do repo (`.gitignore` + variáveis de ambiente).
  :::
- **P:** "Por que usar Docker num pipeline de dados?"
  :::{dropdown} Resposta modelo
  Para reprodutibilidade: o mesmo ambiente (versões de Python, libs, serviços) roda igual em dev, CI e produção, eliminando o "na minha máquina funciona" e facilitando deploy.
  :::

## 🚀 Para ir além (leitura dirigida)
- **MIT — The Missing Semester** (aulas de shell, Git e ferramentas de linha de comando) — prática e aberta.
- **Pro Git**, cap. 2–3 (uso diário e branches) — leitura aberta em português.
- **Docker docs** — "Get started" (imagens, containers, volumes).

## 📚 Referências
- Chacon, S.; Straub, B. *Pro Git*, 2ª ed. (2014) — [leitura aberta](https://git-scm.com/book/pt-br/v2), cap. 1 e 3. <!-- @chacon2014 -->
- MIT. *The Missing Semester of Your CS Education* (2020) — [site aberto](https://missing.csail.mit.edu/). <!-- @mit-missing-semester -->
- Docker. *Documentação oficial* — [docs.docker.com](https://docs.docker.com/). <!-- @docs-docker -->
- Git. *Reference* — [git-scm.com/docs](https://git-scm.com/docs). <!-- @docs-git -->

*Acessado em: 2026-08-21.*

---
**Revisado em:** 2026-08-21
