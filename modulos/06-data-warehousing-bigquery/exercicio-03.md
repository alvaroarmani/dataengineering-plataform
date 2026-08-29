# Exercício 03 — Particionamento no Postgres real (com pytest)

**Onde roda:** 🐳 Bancada Docker (**Postgres real**, não navegador). É o espelho
auto-corrigível do [Lab 03](lab-03-bigquery-na-pratica.md): o mesmo raciocínio de
partição/pruning que você viu no BigQuery, aqui no particionamento **declarativo** do Postgres.

Suba a bancada uma vez:
```bash
cd ambiente && cp .env.example .env && docker compose up -d && cd ..
pip install psycopg2-binary pytest
```

## Tabela
O teste cria uma tabela **particionada por ano**:
`pedidos(ano, mes, categoria, valor)` — `PARTITION BY RANGE (ano)` com partições 2023/2024/2025.

## Tarefas
Edite os dois arquivos SQL da pasta [`exercicio-03/`](exercicio-03/):

- **`consulta_a.sql`** — receita **mensal de 2025**: `(mes, receita)` = `SUM(valor)`, ordenado
  por `mes`. Filtre por `ano = 2025` (a coluna de partição → o Postgres poda as outras).
- **`consulta_b.sql`** — total por ano com `ano >= 2024`: `(ano, receita)`, ordenado por `ano`.

```bash
pytest -q modulos/06-data-warehousing-bigquery/exercicio-03
```
> A fixture faz rollback ao final — o banco não fica sujo. Fora da bancada, o teste faz *skip*.

## Dicas progressivas
:::{dropdown} Dica 1 — pruning por partição
`SELECT mes, SUM(valor) AS receita FROM pedidos WHERE ano = 2025 GROUP BY mes ORDER BY mes`.
:::
:::{dropdown} Dica 2 — range
`WHERE ano >= 2024`, depois `GROUP BY ano ORDER BY ano`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- consulta_a.sql
SELECT mes, SUM(valor) AS receita
FROM pedidos
WHERE ano = 2025
GROUP BY mes
ORDER BY mes;

-- consulta_b.sql
SELECT ano, SUM(valor) AS receita
FROM pedidos
WHERE ano >= 2024
GROUP BY ano
ORDER BY ano;
```
No Postgres, `PARTITION BY RANGE (ano)` cria partições físicas; o filtro `WHERE ano = 2025`
permite ao planejador **podar** (não ler) as partições 2023 e 2024 — o mesmo princípio do
*partition pruning* do BigQuery, agora numa ferramenta real. Veja com `EXPLAIN` que só a
partição `pedidos_2025` é lida.
:::

---
**Revisado em:** 2026-08-24
