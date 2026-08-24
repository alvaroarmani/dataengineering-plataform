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
- **P:** O que é uma surrogate key? / **R:** Inteiro artificial, sequencial e sem significado de negócio, gerado pelo DW; é a chave primária da dimensão.
- **P:** Chave natural vs surrogate? / **R:** Natural (SKU, CPF) vem da origem e tem significado; surrogate é opaca e estável, criada pelo DW. A dimensão guarda as duas; o fato usa a surrogate.
- **P:** Por que o fato referencia a surrogate, não a natural? / **R:** Isola o DW de mudanças na origem, é mais rápida/compacta (inteiro vs string), integra fontes e habilita histórico (SCD2).
- **P:** O que é surrogate key lookup? / **R:** Ao carregar o fato, juntar os dados (com a chave natural) à dimensão pela chave natural para trocá-la pela surrogate key.
- **P:** Por que surrogate key é pré-requisito de SCD2? / **R:** No SCD2 a mesma chave natural tem várias versões/linhas; só a surrogate (única por linha) distingue cada versão.
- **P:** O que é uma Slowly Changing Dimension (SCD)? / **R:** Uma política para tratar mudanças nos atributos de uma dimensão no tempo, preservando (ou não) o histórico conforme o tipo.
- **P:** SCD Tipo 1 vs Tipo 2? / **R:** Tipo 1 sobrescreve (sem histórico); Tipo 2 insere nova linha e encerra a antiga (histórico completo, com surrogate keys e colunas de vigência).
- **P:** O que faz o SCD Tipo 3? / **R:** Guarda o valor anterior numa coluna extra (ex.: cidade_atual + cidade_anterior) — histórico limitado a uma mudança.
- **P:** Colunas típicas de um SCD2? / **R:** valido_de, valido_ate (intervalo de vigência) e uma flag corrente (linha vigente hoje).
- **P:** Como consultar o point-in-time num SCD2? / **R:** WHERE valido_de <= :data AND :data < valido_ate — retorna a versão vigente naquela data.
- **P:** Quando usar Tipo 1? / **R:** Para correções de erro, quando não faz sentido preservar o valor antigo (ex.: um CEP digitado errado).

---
**Revisado em:** 2026-08-22
