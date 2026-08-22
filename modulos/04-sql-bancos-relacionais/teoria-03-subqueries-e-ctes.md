# Subqueries e CTEs: consultas dentro de consultas

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Algumas perguntas têm **duas etapas**: "quais pedidos estão acima da média?" exige primeiro
**calcular a média** e depois **filtrar** por ela. Ou "clientes que gastaram mais que a média
de gasto" — calcular os totais, depois comparar. **Subqueries** e **CTEs** deixam você
compor essas etapas de forma legível, sem sair do SQL.

## 💡 Conceito (o porquê)

### Subquery: uma consulta dentro de outra
```sql
SELECT id, valor
FROM pedidos
WHERE valor > (SELECT AVG(valor) FROM pedidos);   -- subquery escalar
```
A subquery calcula um valor (a média) usado pela consulta externa. Também aparecem em
`FROM` (subquery como tabela) e com `IN` / `EXISTS`.

### CTE: a subquery com nome (WITH)
Uma **CTE** (*Common Table Expression*) dá **nome** a um resultado intermediário, tornando
consultas de várias etapas muito mais legíveis:
```sql
WITH total_por_cliente AS (
    SELECT cliente_id, SUM(valor) AS total
    FROM pedidos
    GROUP BY cliente_id
)
SELECT *
FROM total_por_cliente
WHERE total > (SELECT AVG(total) FROM total_por_cliente)
ORDER BY total DESC;
```
Leia de cima para baixo: primeiro monto `total_por_cliente`, depois consulto sobre ele. É a
forma preferida no dia a dia — mais clara que subqueries aninhadas.

:::{admonition} 💡 CTE > subquery aninhada (legibilidade)
:class: tip
Tudo que uma CTE faz, uma subquery também faz — mas encadear 3 subqueries aninhadas vira
ilegível. CTEs nomeiam cada passo, como variáveis num script. Prefira CTEs para lógica de
várias etapas.
:::

## 🔎 Exemplo
```sql
-- categorias cuja receita passa da metade da maior receita
WITH r AS (
    SELECT categoria, SUM(valor) AS receita FROM pedidos GROUP BY categoria
)
SELECT categoria, receita FROM r
WHERE receita > (SELECT MAX(receita) FROM r) / 2
ORDER BY receita DESC;
```

:::{admonition} 📖 Da literatura
:class: seealso
Tanimura recomenda CTEs para estruturar análises em etapas — cada CTE é um bloco nomeado e
testável, o que torna consultas complexas legíveis e fáceis de depurar. — *SQL for Data Analysis*.
:::

## ⚠️ Erros comuns
- Subquery escalar que retorna **mais de uma linha** onde se espera um valor → erro.
- Repetir a mesma subquery várias vezes em vez de nomeá-la numa CTE.
- Achar que CTE "materializa"/acelera sempre — é sobretudo **legibilidade** (o otimizador decide).
- `NOT IN` com valores `NULL` na subquery → resultado vazio inesperado (prefira `NOT EXISTS`).

## 💼 O que o mercado espera
CTEs são onipresentes em bases modernas (e no dbt, M07). Saber quebrar um problema em etapas
com `WITH` é sinal de SQL maduro e cai em entrevistas de nível Pleno.

:::{admonition} ✨ Em resumo
:class: resumo
- **Subquery** = consulta dentro de outra (em `WHERE`, `FROM`, `IN`/`EXISTS`).
- **CTE (`WITH`)** = subquery **nomeada**; ideal para lógica em várias etapas.
- Prefira **CTEs** à aninhamento profundo (legibilidade e depuração).
- Cuidado com subquery escalar que retorna várias linhas e com `NOT IN` + `NULL`.
:::

## 🧠 Quiz de recall
1. O que é uma CTE e qual sua principal vantagem?
   :::{dropdown} Resposta
   Um resultado intermediário nomeado (`WITH nome AS (...)`); a vantagem é legibilidade — quebra consultas complexas em etapas claras e reutilizáveis.
   :::
2. Onde uma subquery pode aparecer?
   :::{dropdown} Resposta
   No `WHERE` (escalar ou com `IN`/`EXISTS`), no `FROM` (como uma tabela derivada) e até no `SELECT`.
   :::
3. Por que `NOT IN` pode dar problema?
   :::{dropdown} Resposta
   Se a subquery retornar algum `NULL`, o `NOT IN` pode devolver vazio inesperadamente; use `NOT EXISTS` nesses casos.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como listar clientes que gastaram acima da média de gasto?"
  :::{dropdown} Resposta modelo
  Com uma CTE: calcule o total por cliente, depois filtre onde o total é maior que a média dos totais (`WHERE total > (SELECT AVG(total) FROM cte)`).
  :::
- **P:** "CTE é mais rápida que subquery?"
  :::{dropdown} Resposta modelo
  Nem sempre — a diferença principal é legibilidade. O otimizador geralmente trata as duas de forma parecida; em alguns bancos a CTE pode ser materializada, mas não conte com isso para performance.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Tanimura — SQL for Data Analysis**, seções sobre subqueries e CTEs.
- **Docs do PostgreSQL** — WITH Queries (Common Table Expressions).

## 📚 Referências
- Tanimura, C. *SQL for Data Analysis* (O'Reilly, 2021) — subqueries e CTEs. <!-- @tanimura2021 -->
- PostgreSQL. *Documentação oficial* — [WITH Queries (CTEs)](https://www.postgresql.org/docs/current/queries-with.html). <!-- @docs-postgres -->

*Acessado em: 2026-08-22.*

---
**Revisado em:** 2026-08-22
