# Módulo 13 — DataOps, CI/CD e Infraestrutura como Código

> Automação e engenharia de software aplicadas a dados: entregar com confiança e velocidade.

## Identificação
- **Eixo:** 4 — Escala, Qualidade e Governança
- **Carga horária:** 25h
- **Pré-requisitos:** M10, M12
- **Onde roda:** Bancada Docker + GitHub Actions

## Ementa
Princípios de DataOps. Fluxos de Git para times de dados (branching, PRs, revisão).
CI/CD para dados: testar dbt/pipelines automaticamente, ambientes (dev/prod). Introdução a
Infraestrutura como Código com Terraform (recursos, estado, providers). Boas práticas de
versionamento de dados e ambientes.

## Competências e habilidades
- C11 — aplicar DataOps, CI/CD e noções de IaC.

## Objetivos de aprendizagem
1. **Estruturar** um fluxo Git com PRs e revisão para projetos de dados.
2. **Configurar** um pipeline de CI que roda testes (dbt/pytest).
3. **Explicar** IaC e provisionar um recurso simples com Terraform.

## Plano de aulas (unidades)

**Unidade 1 — DataOps e fluxos de Git para dados**
1. **Teoria:** [DataOps e Git para dados](teoria-01-dataops-git.md)
2. **Exercícios:** [Pode fazer merge? (🟢)](exercicio-01.md) · [Ambiente do branch (🟢)](exercicio-02.md)

**Unidade 2 — CI/CD com GitHub Actions**
1. **Teoria:** [CI/CD com GitHub Actions](teoria-02-cicd-github-actions.md)
2. **Artefato real:** [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) — o CI deste repo (linter + build)
3. **Exercícios:** [Rodar pipeline (🟢)](exercicio-03.md) · [Deve deployar? (🟢)](exercicio-04.md)

**Unidade 3 — Introdução a Terraform (IaC)**
1. **Teoria:** [Terraform e Infraestrutura como Código](teoria-03-terraform-iac.md)
2. **Exercícios:** [Plano do Terraform / diff (🟢)](exercicio-05.md) · [Nº de mudanças (🟢)](exercicio-06.md)

> **Módulo completo.** DataOps, CI/CD e IaC — a disciplina que leva dados a produção com segurança.

## Metodologia e avaliação
**Maestria:** repositório com CI que roda testes a cada PR, conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Postura de engenharia (CI, revisão, ambientes) separa Jr de Pleno.

## Erros comuns
- "Deploy" manual sem CI.
- Misturar dev e prod.
- Ignorar o estado do Terraform.

## Recursos
A curar em `recursos.md` (docs do GitHub Actions; docs do Terraform).

---
**Revisado em:** 2026-08-20
