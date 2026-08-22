# JOINs e agregações: cruzando tabelas

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Dados relacionais vivem **espalhados** em várias tabelas — pedidos numa, clientes noutra,
produtos noutra — de propósito (evita repetição). Para responder "quanto cada **cliente**
gastou?", você precisa **juntar** essas tabelas. Isso é o `JOIN`, e dominá-lo é o que
transforma SQL básico em SQL analítico de verdade.

## 💡 Conceito (o porquê)

### O JOIN liga tabelas por uma chave
```sql
SELECT p.id, c.nome, p.valor
FROM pedidos p
JOIN clientes c ON p.cliente_id = c.id;
```
O `ON` diz **como** casar as linhas (a FK de `pedidos` com a PK de `clientes`). Apelidos
(`p`, `c`) deixam a query legível.

### Os tipos que importam
- **`INNER JOIN`** (padrão): só as linhas que casam nos **dois** lados.
- **`LEFT JOIN`**: **todas** as linhas da tabela da esquerda; onde não há par à direita, vem `NULL`.
- `RIGHT`/`FULL`: menos comuns, mas existem.

Regra prática: use `LEFT JOIN` quando quer manter tudo da tabela principal (ex.: todos os
clientes, mesmo os **sem** pedidos).

:::{admonition} 💡 INNER vs LEFT muda o resultado
:class: tip
Um cliente sem nenhum pedido **some** num `INNER JOIN`, mas **aparece** (com `NULL`/0) num
`LEFT JOIN`. Escolher errado silenciosamente perde ou infla dados.
:::

### JOIN + GROUP BY: a dupla analítica
```sql
SELECT c.nome, SUM(p.valor) AS total
FROM pedidos p
JOIN clientes c ON p.cliente_id = c.id
GROUP BY c.nome
ORDER BY total DESC;
```
Junte, agrupe, agregue — é o formato de 80% das perguntas de negócio.

## 🔎 Exemplo
```sql
-- receita por cidade do cliente
SELECT c.cidade, SUM(p.valor) AS receita
FROM pedidos p
JOIN clientes c ON p.cliente_id = c.id
GROUP BY c.cidade
ORDER BY receita DESC;
```

:::{admonition} 📖 Da literatura
:class: seealso
Tanimura mostra que a maioria das análises reais combina `JOIN` (para trazer os atributos
certos) com `GROUP BY` (para resumir) — e alerta que o tipo de join escolhido muda o conjunto
de linhas analisado. — *SQL for Data Analysis*.
:::

## ⚠️ Erros comuns
- Esquecer o `ON` (ou casar pela coluna errada) → **produto cartesiano** (explosão de linhas).
- Usar `INNER` quando queria `LEFT` (perde linhas sem par silenciosamente).
- Agrupar por `c.nome` mas selecionar `c.cidade` fora de agregação → erro.
- `COUNT(coluna)` ignora `NULL`; `COUNT(*)` conta linhas — saiba a diferença.
- Somar valores **depois** de um join que duplicou linhas (contagem inflada).

## 💼 O que o mercado espera
JOIN + GROUP BY é o pão de cada dia e cai em toda entrevista de SQL. Saber quando usar
`LEFT JOIN` (e o efeito nos números) é o que separa quem entende de quem decora.

:::{admonition} ✨ Em resumo
:class: resumo
- `JOIN ... ON` liga tabelas pela chave (FK ↔ PK); use apelidos.
- **`INNER`** = só o que casa; **`LEFT`** = tudo da esquerda + `NULL` onde falta.
- **`JOIN` + `GROUP BY`** resume dados cruzados — o formato analítico mais comum.
- Cuidado com joins que **duplicam** linhas antes de um `SUM`.
:::

## 🧠 Quiz de recall
1. Qual a diferença entre `INNER JOIN` e `LEFT JOIN`?
   :::{dropdown} Resposta
   `INNER` retorna só as linhas que casam nos dois lados; `LEFT` retorna todas as da esquerda, preenchendo com `NULL` onde não há par à direita.
   :::
2. O que causa um "produto cartesiano" e por que é perigoso?
   :::{dropdown} Resposta
   Um join sem condição `ON` (ou com condição errada) combina cada linha de uma tabela com todas as da outra, explodindo o número de linhas e inflando agregações.
   :::
3. `COUNT(*)` vs `COUNT(coluna)`?
   :::{dropdown} Resposta
   `COUNT(*)` conta todas as linhas; `COUNT(coluna)` conta só as linhas em que `coluna` não é `NULL`.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Quando você usaria LEFT JOIN em vez de INNER?"
  :::{dropdown} Resposta modelo
  Quando preciso manter todas as linhas da tabela principal mesmo sem correspondência — ex.: listar todos os clientes e quanto gastaram, inclusive os que gastaram 0 (sem pedidos), que num INNER desapareceriam.
  :::
- **P:** "Um SUM depois de um JOIN veio inflado. O que pode ter acontecido?"
  :::{dropdown} Resposta modelo
  O join provavelmente duplicou linhas (relação 1-para-muitos com outra tabela), fazendo o mesmo valor ser somado várias vezes. Soluções: agregar antes de juntar (subquery/CTE) ou juntar na granularidade certa.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Tanimura — SQL for Data Analysis**, capítulos de JOINs e agregação.
- **pgexercises** — seção de Joins and Subqueries (prática guiada).

## 📚 Referências
- Tanimura, C. *SQL for Data Analysis* (O'Reilly, 2021) — JOINs e agregações. <!-- @tanimura2021 -->
- PostgreSQL. *Documentação oficial* — [Joins](https://www.postgresql.org/docs/current/tutorial-join.html). <!-- @docs-postgres -->
- DuckDB. *Documentação oficial* — [SQL / joins](https://duckdb.org/docs/). <!-- @docs-duckdb -->

*Acessado em: 2026-08-22.*

---
**Revisado em:** 2026-08-22
