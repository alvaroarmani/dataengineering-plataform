# Módulo 10 — Containers e Deploy: Docker avançado

> Empacotar e orquestrar serviços localmente — a base de ambientes reprodutíveis.

## Identificação
- **Eixo:** 3 — Pipelines e Orquestração
- **Carga horária:** 25h
- **Pré-requisitos:** M02
- **Onde roda:** Bancada Docker

## Ementa
Aprofundamento em Docker: escrita de `Dockerfile` (camadas, cache, multi-stage), imagens
enxutas. Redes e volumes. `docker-compose` para múltiplos serviços. Variáveis de ambiente e
segredos. Boas práticas de reprodutibilidade e deploy local. Introdução a registries.

## Competências e habilidades
- C3 — operar ambientes containerizados (nível avançado).

## Objetivos de aprendizagem
1. **Escrever** um `Dockerfile` eficiente (cache, multi-stage).
2. **Orquestrar** múltiplos serviços com `docker-compose` (redes, volumes).
3. **Gerenciar** variáveis de ambiente e segredos com segurança.

## Plano de aulas (unidades)

**Unidade 1 — Dockerfile avançado e imagens enxutas**
1. **Teoria:** [Dockerfile: camadas, cache, imagens enxutas](teoria-01-dockerfile-imagens.md)
2. **Lab (🐳 Docker real):** [Dockerfile multi-stage e cache](lab-01-dockerfile-multistage.md)
3. **Exercícios:** [Cache de camadas (🟢)](exercicio-01.md) · [.dockerignore (🟢)](exercicio-02.md)

**Unidade 2 — Redes, volumes e Compose multi-serviço**
1. **Teoria:** [Redes, volumes e Compose](teoria-02-redes-volumes-compose.md)
2. **Lab (🐳 Docker real):** [Compose multi-serviço: redes e volumes](lab-02-compose-multiservico.md)
3. **Exercícios:** [Ordem de subida (🟢)](exercicio-03.md) · [Mapeamento de portas (🟢)](exercicio-04.md)

**Unidade 3 — Env, segredos, reprodutibilidade e registries**
1. **Teoria:** [Env, segredos e registries](teoria-03-env-segredos-registries.md)
2. **Lab (🐳 Docker real):** [Env, segredos e registry](lab-03-env-registry.md)
3. **Exercícios:** [Resolver env ${VAR:-default} (🟢)](exercicio-05.md) · [Parse de imagem (🟢)](exercicio-06.md)

> **Módulo completo.** Fecha o **Eixo 3 (Pipelines e Orquestração)** — ingestão (M8), orquestração (M9) e containers (M10).

## Metodologia e avaliação
**Maestria:** conteinerizar um pipeline multi-serviço com compose, conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Docker é requisito recorrente; saber orquestrar serviços locais destaca candidatos Jr.

## Erros comuns
- Imagens enormes (sem multi-stage/`.dockerignore`).
- Segredos hardcoded na imagem.
- Não usar volumes para persistência.

## Recursos
A curar em `recursos.md` (docs do Docker; Docker Compose).

---
**Revisado em:** 2026-08-20
