# CI/CD para dados com GitHub Actions

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

O PR (U1) só protege de verdade se **um robô** rodar lint e testes a cada mudança e **barrar** o
que quebra — e, quando aprovado, **entregar** sozinho para produção. Isso é **CI/CD**. Sem ele,
a revisão depende de alguém lembrar de rodar os testes na mão (não roda). Esta unidade mostra o
CI/CD para dados, na prática, com **GitHub Actions**.

## 💡 Conceito (o porquê)

### CI e CD
- **CI (Continuous Integration):** a cada push/PR, um pipeline automático **valida** a mudança —
  instala deps, roda **lint** e **testes** (pytest, `dbt build`, testes de dados do M12). Se algo
  falha, o PR fica **vermelho** e não deve ser mergeado.
- **CD (Continuous Delivery/Deployment):** ao mergear na `main`, um pipeline **entrega** a
  mudança para o ambiente (ex.: `dbt run` em prod, subir a DAG, publicar a imagem). Delivery =
  pronto para deploy com um clique; Deployment = automático.

### GitHub Actions em uma imagem
Um **workflow** é um YAML em `.github/workflows/`. Ele tem:
- **Gatilho (`on`):** quando roda (`push`, `pull_request`, `schedule`).
- **Jobs:** rodam numa VM (`runs-on`), em **steps** (checar o código, instalar, testar).
- Steps usam **actions** prontas (`actions/checkout`, `actions/setup-python`) ou comandos shell.
```yaml
on: [push, pull_request]
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: python scripts/verificar-conteudo.py    # lint de conteúdo
      - run: pytest -q                                # testes
```

### Gates: o que barra o merge
Configura-se a branch `main` como **protegida**: só aceita merge se o CI passou (e houve
revisão). É o "gate" que mantém a `main` sempre verde. **Segredos** (senha do DW, token) ficam
em **GitHub Secrets** (nunca no YAML).

### CI/CD para dados especificamente
Além de lint/pytest: rodar **`dbt build`** (models + testes) contra um ambiente de CI, validar
**DAGs do Airflow** (sem erro de import), rodar **Great Expectations** na ingestão (M12). O deploy
pode aplicar dbt em prod, sincronizar DAGs, ou publicar a imagem (M10) no registry.

## 🔎 Exemplo
Este próprio repositório tem um workflow (`.github/workflows/ci.yml`) que, a cada push/PR, roda
o **linter de conteúdo** e o **pytest** dos exercícios. Se um exercício quebra ou uma teoria
perde referência, o CI fica vermelho — o erro é pego antes do merge, não em produção.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley colocam **CI/CD** no centro do DataOps: automatizar validação e entrega remove o
erro humano ("esqueci de rodar os testes") e torna a `main` sempre deployável — o que permite
entregar mudanças de dados com frequência e segurança. — *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
GitHub Actions (e GitLab CI, etc.) rodam lint + `dbt build` + testes a cada PR e bloqueiam o
merge se algo falha; no merge para `main`, aplicam dbt/atualizam DAGs/publicam imagens. Segredos
vão em Secrets, nunca no YAML. — Reis & Housley (DataOps/CI/CD).
:::

## ⚠️ Erros comuns
- **Sem branch protegida** — dá para mergear vermelho; o CI vira decoração.
- **Segredo no YAML** do workflow — vazamento; use GitHub Secrets.
- CI que **não roda os testes de dados** (dbt/GE) — passa lint mas quebra dados.
- Deploy manual e destreinado — erro humano; automatize o CD.
- Workflows lentos (sem cache de deps) — o time começa a burlar.

## 💼 O que o mercado espera
Ler/escrever um workflow de GitHub Actions que roda lint + testes, entender CI vs CD e branch
protegida é esperado. "Como seu CI valida uma mudança de dbt?" aparece em entrevista de níveis
pleno.

:::{admonition} ✨ Em resumo
:class: resumo
- **CI** valida cada push/PR (lint + testes + `dbt build`); **CD** entrega no merge para `main`.
- **GitHub Actions:** workflow YAML em `.github/workflows/` com `on` (gatilho), `jobs`, `steps`.
- **Branch protegida** só aceita merge com CI verde (+ revisão); **segredos** em GitHub Secrets.
- Para dados: rodar dbt build/testes, validar DAGs, GE na ingestão; deploy aplica em prod.
:::

## 🧠 Quiz de recall
1. Diferença entre CI e CD?
   :::{dropdown} Resposta
   CI valida cada mudança automaticamente (lint/testes) e barra o que quebra; CD entrega a mudança aprovada para o ambiente (delivery = pronto p/ deploy; deployment = automático).
   :::
2. O que compõe um workflow do GitHub Actions?
   :::{dropdown} Resposta
   Um YAML em .github/workflows/ com gatilho (on: push/pull_request/schedule), jobs (runs-on) e steps (checkout, setup, instalar, testar).
   :::
3. Como o CI "barra" um merge ruim?
   :::{dropdown} Resposta
   Com a branch main protegida: o merge só é permitido se o workflow passou (verde) e houve revisão.
   :::
4. Onde ficam os segredos no CI?
   :::{dropdown} Resposta
   Em GitHub Secrets (injetados como variáveis no workflow) — nunca escritos no YAML.
   :::
5. O que um CI de dados roda além de lint/pytest?
   :::{dropdown} Resposta
   dbt build (models + testes), validação de DAGs do Airflow, e/ou Great Expectations na ingestão.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como seu CI valida uma mudança de dbt?"
  :::{dropdown} Resposta modelo
  No PR, um workflow do GitHub Actions faz checkout, instala o dbt, roda `dbt build` (models + testes) contra um ambiente de CI e o linter. Se algo falha, o PR fica vermelho e a branch protegida impede o merge. No merge para main, o CD aplica o dbt em prod. Segredos vêm de GitHub Secrets.
  :::
- **P:** "CI vs CD?"
  :::{dropdown} Resposta modelo
  CI é integração contínua: validar cada mudança (lint/testes/build) automaticamente e barrar o que quebra. CD é entrega/implantação contínua: levar a mudança aprovada ao ambiente — delivery deixa pronto para um deploy de um clique; deployment faz automático.
  :::

## 🚀 Para ir além (leitura dirigida)
- **GitHub Actions docs** — *Workflow syntax*, *Secrets*.
- **Reis & Housley — Fundamentals of Data Engineering** (CI/CD, DataOps).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — CI/CD e DataOps. <!-- @reis2022 -->
- Beauchemin, M. *Functional Data Engineering* (2018) — automação de pipelines. <!-- @beauchemin2018 -->
- Chacon, S.; Straub, B. *Pro Git* (2014) — base de fluxo que o CI automatiza. <!-- @chacon2014 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
