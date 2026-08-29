# Flashcards — Módulo 06

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** OLTP vs OLAP? / **R:** OLTP = transacional (muitas escritas pequenas, roda a operação); OLAP = analítico (leituras que varrem/agregam grandes volumes). Cargas opostas — por isso o DW é separado.
- **P:** O que é um Data Warehouse (Inmon)? / **R:** Coleção de dados orientada a assunto, integrada, não-volátil e variável no tempo (histórica), para análise e decisão.
- **P:** Quais as camadas de um DW? / **R:** Staging/raw (cru), core/integrado (limpo, fonte da verdade), marts/consumo (dimensional para BI). No lakehouse: bronze/prata/ouro.
- **P:** Inmon vs Kimball? / **R:** Inmon = top-down, EDW normalizado primeiro; Kimball = bottom-up, marts dimensionais por processo integrados por dimensões conformadas. Híbridos são comuns.
- **P:** O que é uma dimensão conformada? / **R:** Dimensão compartilhada entre vários fatos/marts (mesma dim_cliente em vendas e devoluções); garante que os números batam e evita ilhas de dados.
- **P:** DW vs data lake? / **R:** Lake guarda dados crus (arquivos, barato/flexível); DW guarda dados modelados e limpos para consulta analítica. Lakehouse une os dois com camadas.
- **P:** Por que não analisar no banco de produção? / **R:** OLTP e OLAP têm cargas antagônicas; consultas analíticas competem com as transações e degradam a operação.
- **P:** Por que o colunar acelera análise? / **R:** Guarda cada coluna separada: lê só as colunas usadas (menos I/O), comprime muito melhor (dados homogêneos) e permite execução vetorizada.
- **P:** Por que evitar SELECT * no DW? / **R:** Força ler todas as colunas do armazenamento colunar, aumentando I/O e (no cloud) o custo por bytes varridos.
- **P:** O que é partition pruning? / **R:** O motor pula partições fora do filtro. Acontece ao filtrar pela coluna de partição (tipicamente data), varrendo muito menos dados.
- **P:** Particionamento vs clustering? / **R:** Particionamento divide fisicamente a tabela (ex.: por mês); clustering ordena dentro da partição por colunas muito filtradas, permitindo pular blocos por mín/máx. Complementares.
- **P:** Dois esquemas de compressão colunar? / **R:** Dictionary encoding (valores repetidos → dicionário+códigos) e RLE (sequências → valor+contagem), que brilha com dados ordenados.
- **P:** No BigQuery, o que reduz custo? / **R:** Ler menos bytes: sem SELECT *, filtrar pela coluna de partição (sem função em cima), particionar por data e clusterizar colunas muito filtradas.
- **P:** O que significa BigQuery ser "serverless"? / **R:** Você não gerencia servidor; separa armazenamento de computação e aloca recursos por query. Paga armazenamento (GB/mês) + bytes varridos.
- **P:** Como praticar BigQuery de graça? / **R:** No BigQuery sandbox — cria projeto e consulta sem cartão, com cotas mensais; tabelas expiram em 60 dias.
- **P:** Para que serve o dry run? / **R:** Estimar os bytes que a query vai varrer (e o custo) ANTES de executar (editor ou `bq query --dry_run`).
- **P:** LIMIT reduz o custo de uma query BigQuery? / **R:** Não — a varredura acontece antes do LIMIT. O que reduz é ler menos colunas e menos partições.
- **P:** Como declarar partição e cluster no BigQuery? / **R:** `PARTITION BY DATE_TRUNC(coluna_data, MONTH)` e `CLUSTER BY col1, col2` na criação da tabela.

---
**Revisado em:** 2026-08-23
