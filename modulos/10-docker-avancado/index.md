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
1. Dockerfile avançado e imagens enxutas.
2. Redes, volumes e compose multi-serviço.
3. Env/segredos e reprodutibilidade; registries.

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
