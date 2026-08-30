# DataOps e fluxos de Git para times de dados

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você já sabe construir pipelines. Mas **como um time entrega mudanças de dados com segurança**,
sem quebrar produção e sem "funciona na minha máquina"? A resposta é **DataOps**: trazer as
práticas de engenharia de software (Git, revisão, testes automáticos, ambientes) para o mundo de
dados. Começa pelo **fluxo de Git** — a base de colaborar sem pisar no pé do outro.

## 💡 Conceito (o porquê)

### DataOps em uma frase
**DataOps** aplica DevOps + controle de qualidade a dados: **versionar** tudo (código, models,
DAGs), **testar** automaticamente (M12), **entregar** por pipelines de CI/CD, em **ambientes**
separados (dev/staging/prod), com **monitoramento**. Objetivo: entregar mudanças de dados
**rápido e com confiança**.

### Git para dados: branches e PRs
- **`main`** = o que está (ou vai) para produção; sempre "verde".
- **Feature branches** (`feature/nova-metrica`): você trabalha isolado, sem afetar a `main`.
- **Pull Request (PR):** propõe juntar sua branch na `main` — abre espaço para **revisão** e
  para o **CI rodar** (lint + testes). Só faz merge se passar.
- **Revisão de código (review):** outra pessoa lê o diff — pega erros, espalha conhecimento.

Isso vale para **dbt models, DAGs, SQL, IaC** — tudo é código versionado. "Versionar o pipeline"
é o que permite reverter, auditar e colaborar.

### Ambientes: dev → staging → prod
A mesma base de código roda em ambientes diferentes: **dev** (você testa), **staging**
(homologação, dados parecidos com prod), **prod** (o real). Costuma-se mapear **branch →
ambiente** (ex.: `main` → prod; `develop` → staging). Config por variável de ambiente (M10), não
hardcoded.

### O que versionar (e o que não)
- **Versione:** código, models, DAGs, SQL, `dbt_project.yml`, IaC, `.env.example`, migrações.
- **Não versione:** segredos (`.env`), dados brutos grandes, artefatos de build — ficam no `.gitignore`.

## 🔎 Exemplo
Uma nova métrica no dbt: você cria `feature/receita-liquida`, escreve o model + teste, abre um
**PR**. O **CI** roda `dbt build`/testes e o linter; um colega revisa. Verde + aprovado → merge
na `main`, que dispara o deploy para prod (M13-U2). Se der ruim, `git revert` volta atrás — nada
disso seria seguro editando direto em produção.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley descrevem **DataOps** como a disciplina de aplicar automação, versionamento,
testes e observabilidade ao ciclo de vida dos dados; Beauchemin (que cunhou "engenharia
funcional de dados") defende tratar pipelines como **código** versionado e testável. —
*Fundamentals of Data Engineering*; *Functional Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Times de dados modernos trabalham como times de software: nada vai para produção sem PR,
revisão e CI verde. `main` protegida, feature branches, e ambientes dev/staging/prod são o
padrão — inclusive para dbt e Airflow. — Reis & Housley (DataOps).
:::

## ⚠️ Erros comuns
- **Editar direto em produção** (no DW/na DAG) — sem revisão, sem histórico, sem volta.
- Commitar **segredos** ou dados grandes — use `.gitignore` (só `.env.example`).
- Branches gigantes de meses — PRs pequenos e frequentes são mais fáceis de revisar.
- `main` sem proteção/CI — quebra de produção passa direto.
- Não separar **ambientes** — testar em prod é receita de incidente.

## 💼 O que o mercado espera
Trabalhar com Git (branch/PR/review), entender DataOps e ambientes dev/staging/prod é **básico**
em qualquer time de dados sério. "Como você leva uma mudança de dbt para produção com segurança?"
é pergunta comum.

:::{admonition} ✨ Em resumo
:class: resumo
- **DataOps** = DevOps + qualidade para dados: versionar, testar, entregar por CI/CD, em ambientes separados.
- **Git flow:** `main` sempre verde; feature branches; **PR** com **revisão** + **CI**; merge só se verde.
- **Ambientes** dev/staging/prod (branch→ambiente); config por env, não hardcoded.
- Versione código/models/DAGs/IaC; **nunca** segredos/dados brutos.
:::

## 🧠 Quiz de recall
1. O que é DataOps?
   :::{dropdown} Resposta
   Aplicar práticas de DevOps + qualidade a dados: versionar tudo, testar automaticamente, entregar por CI/CD, em ambientes separados, com monitoramento — para entregar mudanças rápido e com confiança.
   :::
2. Para que serve um Pull Request?
   :::{dropdown} Resposta
   Propor juntar uma branch na main, abrindo espaço para revisão de código e para o CI rodar (lint/testes); só se faz merge se passar.
   :::
3. Por que feature branches?
   :::{dropdown} Resposta
   Para trabalhar isolado sem afetar a main (que fica sempre verde/deployável) e permitir revisão do diff antes do merge.
   :::
4. Como se mapeiam branches e ambientes?
   :::{dropdown} Resposta
   Comumente main → prod e develop → staging; feature branches em dev. A mesma base de código roda em cada ambiente com config por variável de ambiente.
   :::
5. O que NÃO versionar?
   :::{dropdown} Resposta
   Segredos (.env), dados brutos grandes e artefatos de build — ficam no .gitignore; versione só .env.example e o código/models/DAGs/IaC.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você leva uma mudança de dbt para produção com segurança?"
  :::{dropdown} Resposta modelo
  Numa feature branch: escrevo o model + testes, abro PR. O CI roda dbt build/testes + lint e um colega revisa. Verde + aprovado → merge na main, que dispara o deploy para prod. Ambientes separados (dev/staging/prod) e `git revert` como rede de segurança. Nunca edito direto em produção.
  :::
- **P:** "O que é DataOps na prática?"
  :::{dropdown} Resposta modelo
  Tratar dados como software: versionar código/models/DAGs, testar automaticamente (M12), entregar por CI/CD com PR e revisão, rodar em ambientes dev/staging/prod e monitorar (observabilidade). O objetivo é velocidade com confiança.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (DataOps).
- **Chacon & Straub — Pro Git**, caps. 1–3 (branches, fluxo).
- **Beauchemin — Functional Data Engineering** (pipelines como código).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — DataOps. <!-- @reis2022 -->
- Chacon, S.; Straub, B. *Pro Git*, 2ª ed. (2014) — branches e fluxo de trabalho. <!-- @chacon2014 -->
- Beauchemin, M. *Functional Data Engineering* (2018) — pipelines como código. <!-- @beauchemin2018 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
