# Window functions: cálculos que enxergam as vizinhas

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

`GROUP BY` resume e **colapsa** linhas — você perde o detalhe. Mas muitas perguntas precisam
do detalhe **e** de um cálculo sobre o grupo ao mesmo tempo: "qual a posição de cada pedido
no ranking do seu estado?", "qual o total acumulado dia a dia?", "quanto cada venda
representa do total?". Isso são **window functions** — e elas são o divisor de águas entre
SQL júnior e pleno.

## 💡 Conceito (o porquê)

### A cláusula OVER
Uma window function calcula sobre um "janela" de linhas **sem colapsá-las**:
```sql
SELECT id, estado, valor,
       SUM(valor) OVER (PARTITION BY estado) AS total_estado
FROM pedidos;
```
Cada linha **mantém-se**, mas ganha uma coluna com a soma do seu estado. A mágica está no
`OVER (...)`:
- **`PARTITION BY`** — divide em grupos (como o `GROUP BY`, mas sem colapsar).
- **`ORDER BY`** (dentro do `OVER`) — define a ordem para cálculos posicionais/acumulados.

### As funções que mais aparecem
- **Ranking:** `ROW_NUMBER()` (1,2,3… sem empate), `RANK()` (pula no empate), `DENSE_RANK()`.
- **Agregações em janela:** `SUM/AVG/COUNT ... OVER (...)` (total do grupo, média móvel, acumulado).
- **Deslocamento:** `LAG()` / `LEAD()` — valor da linha anterior/seguinte (ótimo para variação período a período).

### Exemplo de ranking por grupo
```sql
SELECT id, estado, valor,
       ROW_NUMBER() OVER (PARTITION BY estado ORDER BY valor DESC) AS posicao
FROM pedidos;
```
Para pegar o **top 1 de cada estado**, envolva numa subquery/CTE e filtre `posicao = 1`
(não dá para usar a window direto no `WHERE` — ela é calculada depois).

## 🔎 Exemplo — total acumulado
```sql
SELECT id, valor,
       SUM(valor) OVER (ORDER BY id) AS acumulado
FROM pedidos
ORDER BY id;
```

:::{admonition} 📖 Da literatura
:class: seealso
Tanimura dedica atenção especial às window functions por habilitarem análises que o
`GROUP BY` sozinho não faz — rankings, médias móveis e comparações entre linhas — mantendo o
grão original. — *SQL for Data Analysis*.
:::

## ⚠️ Erros comuns
- Tentar filtrar por uma window function no `WHERE` → erro (ela roda **depois**; use subquery/CTE).
- Confundir `ROW_NUMBER` (sempre único) com `RANK` (empata e pula números).
- Esquecer o `ORDER BY` dentro do `OVER` em cálculos acumulados (resultado sem sentido).
- Achar que window "agrupa" — ela **não** reduz o número de linhas (diferente do `GROUP BY`).

## 💼 O que o mercado espera
Window functions caem em quase toda entrevista de SQL de nível Pleno (ranking por grupo,
"top N por categoria", variação mês a mês). Saber usá-las bem é um diferencial claro.

:::{admonition} ✨ Em resumo
:class: resumo
- Window function = cálculo sobre uma janela **sem colapsar** linhas (`... OVER (...)`).
- `PARTITION BY` agrupa; `ORDER BY` (no OVER) ordena para ranking/acumulado.
- `ROW_NUMBER`/`RANK`/`DENSE_RANK`, agregações em janela, `LAG`/`LEAD`.
- Para filtrar por ranking, use subquery/CTE (a window roda depois do WHERE).
:::

## 🧠 Quiz de recall
1. Qual a diferença entre uma agregação com `GROUP BY` e uma window function?
   :::{dropdown} Resposta
   `GROUP BY` colapsa cada grupo em uma linha; a window function calcula sobre o grupo (janela) mas **mantém** todas as linhas, adicionando o resultado como coluna.
   :::
2. `ROW_NUMBER()` vs `RANK()`?
   :::{dropdown} Resposta
   `ROW_NUMBER` numera 1,2,3… sem empates; `RANK` dá o mesmo número a empates e **pula** os seguintes (1,1,3). `DENSE_RANK` empata sem pular (1,1,2).
   :::
3. Como pegar o "top 1 de cada grupo" com window function?
   :::{dropdown} Resposta
   Calcule `ROW_NUMBER() OVER (PARTITION BY grupo ORDER BY metrica DESC)` numa subquery/CTE e filtre `= 1` na consulta externa (não dá para filtrar no WHERE da mesma consulta).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Traga o produto/pedido de maior valor por estado."
  :::{dropdown} Resposta modelo
  `WITH r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY estado ORDER BY valor DESC) AS rn FROM pedidos) SELECT * FROM r WHERE rn = 1;`
  :::
- **P:** "Como calcular a variação de receita mês a mês?"
  :::{dropdown} Resposta modelo
  Agregue receita por mês numa CTE e use `LAG(receita) OVER (ORDER BY mes)` para trazer o mês anterior, depois calcule `receita - lag`.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Tanimura — SQL for Data Analysis**, capítulo de window functions.
- **Docs do PostgreSQL** — Window Functions (tutorial).

## 📚 Referências
- Tanimura, C. *SQL for Data Analysis* (O'Reilly, 2021) — window functions. <!-- @tanimura2021 -->
- PostgreSQL. *Documentação oficial* — [Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html). <!-- @docs-postgres -->

*Acessado em: 2026-08-22.*

---
**Revisado em:** 2026-08-22
