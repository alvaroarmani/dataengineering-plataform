# Flashcards — Módulo 13

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** O que é DataOps? / **R:** DevOps + qualidade para dados: versionar tudo, testar automaticamente, entregar por CI/CD, em ambientes separados, com monitoramento.
- **P:** Para que serve um Pull Request? / **R:** Propor merge de uma branch na main, com revisão + CI; só mescla se verde.
- **P:** Branches e ambientes? / **R:** Comumente main→prod, develop→staging, feature/*→dev; mesma base, config por env.
- **P:** CI vs CD? / **R:** CI valida cada mudança (lint/testes/build) e barra o que quebra; CD entrega a mudança aprovada ao ambiente.
- **P:** O que compõe um workflow do GitHub Actions? / **R:** YAML em .github/workflows/ com gatilho (on), jobs (runs-on) e steps (checkout, setup, testar).
- **P:** Onde ficam segredos no CI? / **R:** Em GitHub Secrets — nunca no YAML.
- **P:** O que é IaC? / **R:** Declarar a infra em código versionado (Terraform) em vez de clicar no console — reprodutível, auditável.
- **P:** plan vs apply no Terraform? / **R:** plan mostra o diff (criar/atualizar/destruir) sem aplicar; apply executa.
- **P:** O que é o state do Terraform? / **R:** O mapa entre código e recursos reais; comparando-o com o código, calcula o diff. Fica remoto e travado.
- **P:** Por que apply é idempotente? / **R:** Rodar de novo sem mudar o código não faz nada — a infra já bate com o desejado.

---
**Revisado em:** 2026-08-29
