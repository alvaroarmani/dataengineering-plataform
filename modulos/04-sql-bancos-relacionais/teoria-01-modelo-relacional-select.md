# SQL do zero: modelo relacional e o SELECT

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Quase todo dado importante de uma empresa vive num **banco relacional** — tabelas com linhas
e colunas. **SQL** é a língua para conversar com esses dados, e é, disparado, a competência
mais pedida em vagas de dados. A boa notícia: SQL é **declarativo** — você diz *o que* quer,
não *como* buscar. Este é o primeiro passo: entender o modelo relacional e escrever o
`SELECT`.

## 💡 Conceito (o porquê)

### O modelo relacional
Os dados são organizados em **tabelas** (relações). Cada **linha** é um registro; cada
**coluna** tem um tipo. Duas ideias-chave:
- **Chave primária (PK):** identifica cada linha de forma única (ex.: `pedido_id`).
- **Chave estrangeira (FK):** aponta para a PK de outra tabela, ligando-as (ex.: `cliente_id`
  numa tabela de pedidos referencia a tabela de clientes).

Isso evita repetição (normalização, M05) e mantém a integridade dos dados.

### O SELECT: a espinha dorsal
```sql
SELECT estado, valor        -- quais colunas
FROM pedidos                -- de qual tabela
WHERE valor > 100           -- filtro (linhas)
ORDER BY valor DESC         -- ordenação
LIMIT 10;                   -- quantas linhas
```

- **`WHERE`** filtra linhas com condições (`=`, `>`, `<`, `<>`, `AND`, `OR`, `IN`, `BETWEEN`, `LIKE`).
- **`ORDER BY`** ordena (`ASC` padrão, `DESC` decrescente).
- **`LIMIT`** corta o número de linhas.
- **`DISTINCT`** remove duplicatas: `SELECT DISTINCT estado FROM pedidos`.

### Agregar: `COUNT`, `SUM`, `AVG` + `GROUP BY`
Resumir dados por grupo — o coração da análise:
```sql
SELECT estado, COUNT(*) AS n, SUM(valor) AS receita
FROM pedidos
GROUP BY estado
ORDER BY receita DESC;
```
Isto lê como uma frase: "para cada estado, conte os pedidos e some o valor".

:::{admonition} 💡 A ordem lógica não é a ordem escrita
:class: tip
Você escreve `SELECT ... FROM ... WHERE ... GROUP BY ...`, mas o banco executa mais ou menos
nesta ordem: **FROM → WHERE → GROUP BY → SELECT → ORDER BY → LIMIT**. Por isso um apelido
criado no `SELECT` nem sempre pode ser usado no `WHERE`.
:::

## 🔎 Exemplo
```sql
-- receita por categoria, só de SP, top 3
SELECT categoria, SUM(valor) AS receita
FROM pedidos
WHERE estado = 'SP'
GROUP BY categoria
ORDER BY receita DESC
LIMIT 3;
```

:::{admonition} 📖 Da literatura
:class: seealso
Tanimura trata o `SELECT` com `GROUP BY` como a base da análise em SQL — a maioria das
perguntas de negócio é uma variação de "agrupe por X e agregue Y". — *SQL for Data Analysis*.
:::

## ⚠️ Erros comuns
- Confundir **`WHERE`** (filtra linhas **antes** de agrupar) com **`HAVING`** (filtra grupos **depois**).
- Selecionar uma coluna que não está no `GROUP BY` nem numa função de agregação → erro.
- Esquecer que `NULL` não é igual a nada: use `IS NULL` / `IS NOT NULL`, não `= NULL`.
- `LIKE` sem `%` (curinga): `LIKE 'a%'` (começa com a) vs `= 'a'`.
- Achar que `ORDER BY` deixa a consulta "sempre ordenada" — sem ele, a ordem **não é garantida**.

## 💼 O que o mercado espera
Fluência em `SELECT`/`WHERE`/`GROUP BY`/`ORDER BY` é o **mínimo** cobrado em qualquer
entrevista de dados — normalmente com SQL ao vivo. É a base de tudo que vem depois.

:::{admonition} ✨ Em resumo
:class: resumo
- Dados relacionais = **tabelas** ligadas por **PK/FK**.
- `SELECT colunas FROM tabela WHERE filtro ORDER BY ... LIMIT n`.
- **`GROUP BY` + agregações** (COUNT/SUM/AVG) respondem a maioria das perguntas.
- `WHERE` filtra linhas; `HAVING` filtra grupos; `NULL` se testa com `IS NULL`.
:::

## 🧠 Quiz de recall
1. Qual a diferença entre `WHERE` e `HAVING`?
   :::{dropdown} Resposta
   `WHERE` filtra **linhas** antes do agrupamento; `HAVING` filtra **grupos** depois do `GROUP BY` (ex.: `HAVING SUM(valor) > 1000`).
   :::
2. Como somar o valor por estado?
   :::{dropdown} Resposta
   `SELECT estado, SUM(valor) FROM pedidos GROUP BY estado`.
   :::
3. Por que `coluna = NULL` não funciona?
   :::{dropdown} Resposta
   `NULL` representa "desconhecido"; qualquer comparação com `=` resulta em `NULL` (nem verdadeiro). Use `IS NULL` / `IS NOT NULL`.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Escreva uma query que traga os 5 clientes que mais gastaram."
  :::{dropdown} Resposta modelo
  `SELECT cliente_id, SUM(valor) AS total FROM pedidos GROUP BY cliente_id ORDER BY total DESC LIMIT 5;`
  :::
- **P:** "Por que SQL é chamado de linguagem declarativa?"
  :::{dropdown} Resposta modelo
  Porque você descreve **o que** quer (o resultado), não **como** computá-lo. O otimizador do banco decide o plano de execução (que índices usar, ordem de operações), diferente de código imperativo.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Tanimura — SQL for Data Analysis**, caps. iniciais (SELECT, agregações).
- **Docs do PostgreSQL** — tutorial de consultas; **Docs do DuckDB** — para praticar no navegador.

## 📚 Referências
- Tanimura, C. *SQL for Data Analysis* (O'Reilly, 2021) — SELECT e agregações. <!-- @tanimura2021 -->
- PostgreSQL. *Documentação oficial* — [Tutorial / Queries](https://www.postgresql.org/docs/current/tutorial.html). <!-- @docs-postgres -->
- DuckDB. *Documentação oficial* — [SQL introduction](https://duckdb.org/docs/). <!-- @docs-duckdb -->

*Acessado em: 2026-08-22.*

---
**Revisado em:** 2026-08-22
