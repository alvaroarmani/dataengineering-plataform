# Git em profundidade: commits, branches e colaboração

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Todo o seu trabalho de dados — pipelines, models dbt, DAGs, DDLs — é **código**, e código sem controle
de versão é uma bomba-relógio: "qual era a versão que funcionava?", "quem mudou isso?", "como reverto
sem quebrar o resto?". Salvar `pipeline_final_v3_ok.py` não é versionamento — é caos. **Git** resolve:
guarda o **histórico completo** do projeto, deixa você experimentar sem medo (branches), reverter com
segurança e **colaborar** sem sobrescrever o trabalho do outro. Git não é "coisa de dev" — é a base do
DataOps (M13), do CI/CD e de qualquer portfólio no GitHub (M15). Dominar o essencial é inegociável.

## 💡 Conceito (o porquê)

### O commit: um retrato versionado
Um **commit** é um **retrato (snapshot)** do projeto num instante, com um autor, uma data e uma
**mensagem** que explica o *porquê* da mudança. A sequência de commits é o histórico — você pode voltar
a qualquer ponto. Bons commits são **pequenos e coesos** (uma mudança lógica cada) e têm mensagens
claras. O padrão **Conventional Commits** ajuda: `feat: ...`, `fix: ...`, `docs: ...` — o tipo diz de
relance o que mudou (e alimenta changelogs automáticos).

### O fluxo local: working → staging → commit
O Git tem três áreas:
1. **Working directory:** seus arquivos como estão agora.
2. **Staging area (index):** o que você **selecionou** para o próximo commit (`git add`).
3. **Repositório:** o histórico gravado (`git commit`).

Esse `add` → `commit` deixa você montar um commit **deliberado** (só as mudanças relacionadas), em vez
de fotografar tudo de qualquer jeito. `git status` mostra em que área cada arquivo está.

### Branches: experimentar sem medo
Uma **branch** é uma linha de trabalho paralela. Você cria uma (`feature/nova-dag`), trabalha isolado, e
só depois **integra** na principal (`main`). Isso permite desenvolver várias coisas ao mesmo tempo, sem
quebrar o que está em produção. Integrar é o **merge** (ou, num fluxo de time, o **Pull Request** no
GitHub, com revisão + CI antes de entrar — M13).

### Conflitos e como não entrar em pânico
Quando duas branches mudam a **mesma linha**, o merge gera um **conflito**: o Git não adivinha qual
versão vale e marca o trecho (`<<<<<<<`, `=======`, `>>>>>>>`) para **você** decidir. Conflito é normal,
não erro — você edita, escolhe o certo, e conclui o merge. Commits pequenos e branches curtas reduzem
conflitos.

### O que NÃO versionar (.gitignore)
Nem tudo vai para o Git. **Segredos** (`.env`, chaves — M14), **artefatos gerados** (`__pycache__/`,
`.venv/`, `target/` do dbt) e **dados grandes** ficam de fora, via `.gitignore`. Versionar um segredo é
um vazamento (e ele fica no histórico para sempre); versionar gerados polui o repo. Regra: versione a
**fonte** (código, config, o script que baixa os dados), não o **derivado**.

## 🔎 Exemplo
Você vai adicionar uma DAG. Cria a branch `feature/dag-vendas`, escreve o arquivo, e faz
`git add dags/vendas.py` (staging só o que interessa) + `git commit -m "feat: DAG de vendas diárias"`.
Enquanto isso, um `.gitignore` mantém `.env` e `__pycache__/` fora. Termina, abre um **Pull Request** no
GitHub; o **CI** (M13) roda os testes; um colega revisa; o merge entra na `main`. Se houvesse um conflito
com outra mudança na mesma linha, o Git marcaria o trecho e você resolveria manualmente. Histórico
limpo, nada sobrescrito, segredos protegidos.

## ⚠️ Erros comuns
- **Commits gigantes** ("mexi em tudo") — difíceis de revisar e reverter; prefira pequenos e coesos.
- **Mensagens vagas** ("update", "ajustes") — não dizem o *porquê*; use Conventional Commits.
- **Versionar segredos** (`.env`, chaves) — vazamento que fica no histórico; use `.gitignore` e rotacione se acontecer.
- **Trabalhar direto na `main`** sem branch — quebra a base e atrapalha a colaboração.
- **Ter medo de conflito** — é normal; o Git só está pedindo para você decidir qual versão vale.

## 💼 O que o mercado espera
Usar Git com fluência: staging deliberado, commits pequenos com boas mensagens, branches + Pull
Requests, resolver conflitos e um `.gitignore` correto. É pré-requisito de qualquer vaga e a base do
DataOps (M13) e do portfólio (M15). "Como você organiza seu fluxo de Git?" aparece em entrevista.

:::{admonition} ✨ Em resumo
:class: resumo
- **Commit** = snapshot com mensagem; prefira **pequenos e coesos** (Conventional Commits).
- Fluxo local **working → staging (`add`) → commit**; `git status` mostra onde cada arquivo está.
- **Branch** isola o trabalho; integra-se por **merge/Pull Request** (com revisão + CI).
- **Conflito** é normal (o Git pede sua decisão); **`.gitignore`** mantém segredos e gerados fora do repo.
:::

## 🧠 Quiz de recall
1. O que é um commit e como deve ser?
   :::{dropdown} Resposta
   Um snapshot do projeto num instante, com autor, data e mensagem. Deve ser pequeno e coeso (uma mudança lógica), com mensagem clara do porquê (ex.: Conventional Commits).
   :::
2. Quais as três áreas do fluxo local do Git?
   :::{dropdown} Resposta
   Working directory (arquivos atuais), staging area (o que foi selecionado com `git add` para o próximo commit) e repositório (o histórico gravado com `git commit`).
   :::
3. Para que serve uma branch?
   :::{dropdown} Resposta
   Isolar uma linha de trabalho paralela para experimentar/desenvolver sem quebrar a `main`; depois integra-se por merge ou Pull Request.
   :::
4. O que é um conflito de merge e o que fazer?
   :::{dropdown} Resposta
   Quando duas branches mudam a mesma linha; o Git marca o trecho e você decide manualmente qual versão vale, então conclui o merge. É normal, não um erro.
   :::
5. O que NÃO deve ser versionado, e por quê?
   :::{dropdown} Resposta
   Segredos (.env, chaves), artefatos gerados (__pycache__, .venv, target) e dados grandes — via .gitignore. Segredo versionado vaza e fica no histórico; gerados poluem o repo.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você organiza seu fluxo de Git num projeto de dados?"
  :::{dropdown} Resposta modelo
  Trabalho em branches curtas por mudança (`feature/...`), com commits pequenos e mensagens no padrão Conventional Commits. Faço `git add` só do que é relacionado (staging deliberado) e abro Pull Requests para revisão + CI antes de integrar na `main`. Mantenho um `.gitignore` sólido (segredos, gerados, dados grandes fora) e resolvo conflitos com calma. Isso dá histórico limpo, colaboração sem sobrescrita e a base para DataOps.
  :::
- **P:** "Você commitou um `.env` com uma senha por engano. O que faz?"
  :::{dropdown} Resposta modelo
  Considero a senha comprometida e a **rotaciono imediatamente** (ela fica no histórico do Git mesmo após remover o arquivo). Removo o `.env` do rastreamento, adiciono ao `.gitignore`, e — se necessário — reescrevo o histórico para expurgar o segredo. Depois previno com um scan de segredos no CI. É o mesmo princípio de segurança do M14.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Chacon & Straub — Pro Git** (o livro-referência, aberto e gratuito).
- **Documentação oficial do Git** — <https://git-scm.com/doc>.
- **Conventional Commits** — <https://www.conventionalcommits.org/> (padrão de mensagens).

## 📚 Referências
- Chacon, S.; Straub, B. *Pro Git* (2014) — commits, branches, fluxo. <!-- @chacon2014 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — versionamento e DataOps. <!-- @reis2022 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
