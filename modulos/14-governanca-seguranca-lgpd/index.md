# Módulo 14 — Governança, Segurança e LGPD/GDPR

> Dados são responsabilidade: proteger, catalogar e cumprir a lei.

## Identificação
- **Eixo:** 4 — Escala, Qualidade e Governança
- **Carga horária:** 20h
- **Pré-requisitos:** M06
- **Onde roda:** Conceitual + Bancada Docker

## Ementa
Governança de dados: catálogo, lineage, ownership, glossário de negócio. Segurança:
controle de acesso, criptografia, mascaramento, princípio do menor privilégio. Privacidade
e a **LGPD** (e paralelos com a GDPR): dados pessoais/sensíveis, bases legais, direitos do
titular, anonimização vs pseudonimização. Impacto no ciclo de vida do dado.

## Competências e habilidades
- C12 — aplicar governança, segurança e LGPD.

## Objetivos de aprendizagem
1. **Identificar** dados pessoais/sensíveis num dataset.
2. **Aplicar** mascaramento/anonimização e controle de acesso.
3. **Explicar** obrigações da LGPD relevantes à engenharia de dados.
4. **Descrever** o papel de catálogo e lineage na governança.

## Plano de aulas (unidades)

**Unidade 1 — Governança: catálogo, lineage, ownership**
1. **Teoria:** [Governança: catálogo, lineage e ownership](teoria-01-governanca-catalogo-lineage.md)
2. **Exercícios:** [Impact analysis / lineage (🟢)](exercicio-01.md) · [Tabelas sem dono (🟢)](exercicio-02.md)

**Unidade 2 — Segurança: acesso, criptografia, mascaramento**
1. **Teoria:** [Segurança: acesso, criptografia e mascaramento](teoria-02-seguranca-acesso-criptografia.md)
2. **Exercícios:** [Mascarar email (🟢)](exercicio-03.md) · [Controle de acesso / RBAC (🟢)](exercicio-04.md)

**Unidade 3 — LGPD/GDPR: privacidade e compliance**
1. **Teoria:** [Privacidade e compliance: LGPD e GDPR](teoria-03-lgpd-gdpr-privacidade.md)
2. **Exercícios:** [Classificar dado LGPD (🟢)](exercicio-05.md) · [Anonimizar registro (🟢)](exercicio-06.md)

> **Módulo completo.** Encerra o Eixo 4 — a disciplina de tratar dados com responsabilidade legal e técnica.

## Metodologia e avaliação
**Maestria:** classificar dados sensíveis de um dataset e propor tratamento (mascaramento/acesso), conforme rubrica.

## O que o mercado espera
Consciência de LGPD e segurança é esperada; erros aqui têm custo legal.

## Erros comuns
- Logar dados pessoais.
- Acesso amplo demais ("todo mundo admin").
- Confundir anonimização com pseudonimização.

## Recursos
A curar em `recursos.md` (texto da LGPD; guias da ANPD; docs de IAM cloud).

---
**Revisado em:** 2026-08-20
