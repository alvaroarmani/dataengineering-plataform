# Índices e performance: por que uma query é lenta

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Uma query que roda em 50 ms com mil linhas pode levar minutos com milhões. Entender **por que**
— e como um **índice** muda o jogo — é o que separa quem "escreve SQL que funciona" de quem
"escreve SQL que escala". Você não precisa ser DBA, mas precisa saber **ler um plano de
execução** e reconhecer os gargalos clássicos.

## 💡 Conceito (o porquê)

### Full scan vs. índice
Sem índice, para achar `WHERE cliente_id = 42` o banco faz um **full table scan** — lê a
tabela inteira. Um **índice** é como o índice remissivo de um livro: uma estrutura (tipicamente
uma **B-tree**) que leva direto às linhas certas, transformando uma busca linear (O(n)) em
algo próximo de O(log n).

```sql
CREATE INDEX idx_pedidos_cliente ON pedidos (cliente_id);
```

### Índices não são de graça
- **Aceleram leituras** por aquela coluna (filtros, joins, ordenação).
- **Custam nas escritas** (cada `INSERT`/`UPDATE` precisa atualizar o índice) e ocupam espaço.
- Regra: indexe colunas muito usadas em `WHERE`, `JOIN` e `ORDER BY` — não tudo.

### Ler o plano de execução: EXPLAIN
`EXPLAIN` (e `EXPLAIN ANALYZE`, que executa e mede) mostra **como** o banco pretende rodar a
query: se faz *scan* ou usa índice, a ordem dos joins, e onde está o custo.

```sql
EXPLAIN SELECT * FROM pedidos WHERE cliente_id = 1;
```
Aprender a ler isso é a habilidade de otimização mais transferível — vale em Postgres,
BigQuery, DuckDB, todos.

### Gargalos clássicos
- Filtro/join em coluna **sem índice** → full scan.
- Função na coluna do filtro (`WHERE lower(nome) = 'ana'`) **anula** o índice.
- `SELECT *` trazendo colunas que você nem usa (mais I/O; em colunar, custa caro).
- Join que **explode** linhas antes de agregar.

## 🔎 Exemplo — antes e depois
```sql
EXPLAIN ANALYZE SELECT * FROM pedidos WHERE cliente_id = 1;   -- full scan
CREATE INDEX idx_cli ON pedidos(cliente_id);
EXPLAIN ANALYZE SELECT * FROM pedidos WHERE cliente_id = 1;   -- usa o índice
```

:::{admonition} 📖 Da literatura
:class: seealso
A documentação do PostgreSQL trata índices como a principal ferramenta para melhorar
desempenho de consultas, enfatizando que devem ser criados de forma **seletiva** — os ganhos
de leitura vêm com custo de escrita e manutenção. — *PostgreSQL — Indexes*.
:::

## ⚠️ Erros comuns
- Indexar **tudo** (degrada escritas e desperdiça espaço) ou **nada** (full scans).
- Aplicar função na coluna do `WHERE` e anular o índice.
- `SELECT *` por padrão em vez de pedir só as colunas necessárias.
- Otimizar "no achismo" sem olhar o `EXPLAIN`.
- Ignorar que o **grão do join** pode inflar linhas e distorcer agregações.

## 💼 O que o mercado espera
Não esperam que você seja DBA, mas sim que você **saiba diagnosticar** uma query lenta: ler o
`EXPLAIN`, propor um índice, evitar full scans e `SELECT *`. Isso aparece em entrevistas Pleno.

:::{admonition} ✨ Em resumo
:class: resumo
- Sem índice = **full scan** (O(n)); índice (B-tree) leva direto às linhas (~O(log n)).
- Índices aceleram **leituras** mas custam **escritas**/espaço — use de forma **seletiva**.
- **`EXPLAIN`/`EXPLAIN ANALYZE`** mostra o plano — a habilidade de otimização mais transferível.
- Evite função na coluna do filtro e `SELECT *` desnecessário.
:::

## 🧠 Quiz de recall
1. O que um índice faz e qual seu custo?
   :::{dropdown} Resposta
   Acelera buscas/joins/ordenações por uma coluna (evita full scan), ao custo de tornar escritas mais lentas e ocupar espaço. Por isso, use seletivamente.
   :::
2. Para que serve o `EXPLAIN`?
   :::{dropdown} Resposta
   Mostra o plano de execução da query (scan vs índice, ordem de joins, custos), ajudando a diagnosticar e otimizar. `EXPLAIN ANALYZE` executa e mede de fato.
   :::
3. Por que `WHERE lower(nome) = 'ana'` pode ser lento mesmo com índice em `nome`?
   :::{dropdown} Resposta
   Aplicar uma função na coluna impede o uso do índice comum (o índice é sobre `nome`, não sobre `lower(nome)`); seria preciso um índice funcional/expressão.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Uma query com `WHERE cliente_id = X` está lenta numa tabela grande. O que você faz?"
  :::{dropdown} Resposta modelo
  Rodo `EXPLAIN` para confirmar full scan; crio um índice em `cliente_id`; verifico se o filtro não aplica função na coluna; e evito `SELECT *`, trazendo só as colunas necessárias. Reavalio o plano depois.
  :::
- **P:** "Por que não indexar todas as colunas?"
  :::{dropdown} Resposta modelo
  Cada índice torna INSERT/UPDATE/DELETE mais lentos (precisam ser atualizados) e ocupa espaço; muitos índices raramente usados só atrapalham. Indexa-se o que é frequentemente filtrado/juntado/ordenado.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Docs do PostgreSQL** — Indexes e Using EXPLAIN.
- **Docs do DuckDB** — `EXPLAIN` / `EXPLAIN ANALYZE`.

## 📚 Referências
- PostgreSQL. *Documentação oficial* — [Indexes](https://www.postgresql.org/docs/current/indexes.html) e [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html). <!-- @docs-postgres -->
- DuckDB. *Documentação oficial* — [EXPLAIN](https://duckdb.org/docs/). <!-- @docs-duckdb -->

*Acessado em: 2026-08-22.*

---
**Revisado em:** 2026-08-22
