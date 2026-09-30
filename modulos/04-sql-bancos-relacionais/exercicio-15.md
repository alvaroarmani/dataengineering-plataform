# Exercício 15 — SQL em corridas reais de táxi de NY (mini-caso · dados reais)

**Onde roda:** 🟢 Browser ou 🐳 Bancada (DuckDB). **Dados reais:** amostra reproduzível de 2.617
corridas de jan/2024 da TLC de Nova York + a tabela oficial de 265 zonas —
[`datasets/amostras/`](../../datasets/amostras/) (gerada por `datasets/gerar_amostras.py`).

## Contexto
Primeiro dia no time de dados de mobilidade. A gerente pede quatro respostas para a reunião de
amanhã — e cada uma exercita uma ferramenta do módulo:

| Pergunta de negócio | Ferramenta de SQL |
|---|---|
| A) Onde mais se embarca? | `JOIN` + `GROUP BY` + desempate no `ORDER BY` |
| B) Em que hora o ticket médio é maior? | `EXTRACT` + `HAVING` (corta amostra pequena) |
| C) Qual a zona campeã de receita em cada borough? | top-1 por grupo com `ROW_NUMBER()` |
| D) Quanto da base é confiável? | `CASE` com prioridade + % com window sobre agregado |

Os dados são **reais**, com os defeitos da base oficial: tarifas negativas (estornos),
desembarques antes do embarque e passageiros nulos. E a tabela de zonas tem dois "desconhecidos":
o borough `'Unknown'` (zona 264) e o borough `'N/A'` (zona 265, "Outside of NYC").

Os testes rodam cada query em **duas bases** — a amostra inteira e só o fornecedor 2 — então só
passa a query que de fato responde à pergunta.

## Tarefa
Preencha `CONSULTA_A` a `CONSULTA_D` em [`exercicio-15/solucao.py`](exercicio-15/solucao.py) (os
comentários de cada uma dizem colunas, filtro e ordenação exatos).

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-15
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — A e B
A: `FROM corridas c JOIN zonas z ON z.LocationID = c.PULocationID`, filtre `total_amount > 0`,
agrupe por zona **e** borough, `ORDER BY corridas DESC, zona LIMIT 5`. O segundo critério do
`ORDER BY` garante um resultado **determinístico** mesmo quando duas zonas empatam.
B: `EXTRACT(hour FROM tpep_pickup_datetime) AS hora`; o filtro por contagem é `HAVING COUNT(*) >= 100`
(não dá para usar `WHERE` com agregado).
:::
:::{dropdown} Dica 2 — C (top-1 por grupo)
Monte em duas CTEs: `por_zona` (receita por borough+zona) e `ranqueado`, com
`ROW_NUMBER() OVER (PARTITION BY borough ORDER BY receita DESC, zona) AS rn`. No fim, `WHERE rn = 1`.
Exclua os desconhecidos com `z.Borough NOT IN ('Unknown', 'N/A')`.
:::
:::{dropdown} Dica 3 — D (prioridade e percentual)
Um `CASE` avalia os `WHEN` **em ordem** e para no primeiro verdadeiro — é assim que se implementa
prioridade. Para o percentual, uma window sobre o agregado:
`ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2)`. Cuidado com `100` inteiro: use `100.0`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- A) JOIN + GROUP BY: agrupe por tudo o que aparece no SELECT sem agregação
SELECT z.Zone AS zona, z.Borough AS borough, COUNT(*) AS corridas,
       ROUND(SUM(c.total_amount), 2) AS receita
FROM corridas c
JOIN zonas z ON z.LocationID = c.PULocationID
WHERE c.total_amount > 0
GROUP BY z.Zone, z.Borough
ORDER BY corridas DESC, zona          -- desempate determinístico
LIMIT 5;

-- B) HAVING filtra GRUPOS (depois do GROUP BY); WHERE filtra LINHAS (antes)
SELECT EXTRACT(hour FROM tpep_pickup_datetime) AS hora, COUNT(*) AS corridas,
       ROUND(AVG(total_amount), 2) AS ticket_medio
FROM corridas
WHERE total_amount > 0
GROUP BY hora
HAVING COUNT(*) >= 100
ORDER BY ticket_medio DESC, hora;

-- C) top-1 por grupo: agregue, numere dentro do grupo, filtre rn = 1
WITH por_zona AS (
    SELECT z.Borough AS borough, z.Zone AS zona, ROUND(SUM(c.total_amount), 2) AS receita
    FROM corridas c JOIN zonas z ON z.LocationID = c.PULocationID
    WHERE c.total_amount > 0 AND z.Borough NOT IN ('Unknown', 'N/A')
    GROUP BY z.Borough, z.Zone
), ranqueado AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY borough ORDER BY receita DESC, zona) AS rn
    FROM por_zona
)
SELECT borough, zona, receita FROM ranqueado WHERE rn = 1 ORDER BY borough;

-- D) CASE com prioridade + window sobre o agregado (SUM(COUNT(*)) OVER () = total geral)
SELECT CASE
         WHEN total_amount <= 0 THEN 'tarifa_nao_positiva'
         WHEN tpep_dropoff_datetime < tpep_pickup_datetime THEN 'desembarque_antes'
         WHEN passenger_count IS NULL THEN 'passageiros_nulo'
         ELSE 'ok'
       END AS situacao,
       COUNT(*) AS corridas,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM corridas
GROUP BY situacao
ORDER BY corridas DESC, situacao;
```

**O que os resultados contam:** o Upper East Side South lidera em volume, mas não é a campeã de
receita de Manhattan em C — é o Midtown Center. E o JFK, só 3º em volume, fatura **quase 4×** o
Midtown: corrida de aeroporto é longa. Volume (A) e receita (C) contam histórias diferentes. E em D,
repare que no fornecedor 2 **não existe** `desembarque_antes`: o defeito de relógio é de um
fornecedor só — o tipo de achado que vira conversa com o provedor dos dados (M12).

**Por que `ROW_NUMBER` e não `RANK`?** Com empate de receita, `RANK` devolveria duas zonas para o
mesmo borough; `ROW_NUMBER` + critério de desempate garante exatamente uma.
:::

---
**Revisado em:** 2026-09-29
