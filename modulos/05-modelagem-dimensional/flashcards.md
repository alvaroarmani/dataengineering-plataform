# Flashcards — Módulo 05

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** Fato vs dimensão? / **R:** Fato = eventos mensuráveis (métricas + chaves), tabela grande; dimensão = contexto descritivo (atributos textuais), tabela pequena e larga.
- **P:** O que é o "grão" de uma fato? / **R:** O que uma linha da tabela fato representa (ex.: um item de pedido). Deve ser declarado primeiro e mantido consistente.
- **P:** Os 4 passos de Kimball? / **R:** 1) processo de negócio; 2) grão; 3) dimensões; 4) fatos (métricas).
- **P:** O que é um star schema? / **R:** Fato central ligado diretamente às dimensões (desnormalizadas), formando uma estrela — simples e rápido de consultar.
- **P:** Star vs snowflake? / **R:** Snowflake normaliza as dimensões em subtabelas (mais JOINs); Kimball prefere star (desnormalizado) pela simplicidade e performance.
- **P:** Por que desnormalizar em OLAP? / **R:** Leitura/análise domina; menos JOINs = consultas simples e rápidas, entendíveis pelo negócio. Repetição de texto é barata.
- **P:** Por que a dim_data é quase sempre necessária? / **R:** Quase toda análise é temporal; uma dimensão de data rica habilita cortes por dia/mês/ano/feriado sem recalcular.
- **P:** Onde vão métricas e onde vão atributos descritivos? / **R:** Métricas numéricas no fato; atributos textuais/descritivos nas dimensões.

---
**Revisado em:** 2026-08-22
