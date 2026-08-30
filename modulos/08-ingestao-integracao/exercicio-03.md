# Exercício 03 — Dedup de reentrega (TRACK REAL · Postgres)

**Onde roda:** 🐳 Bancada Docker (Postgres real). Sem bancada? Faça o [Exercício 04](exercicio-04.md)
(mesma lógica, no navegador).

Um arquivo foi reentregue e duplicou linhas por `id`. Fique com a **versão mais recente**.

## Tabela (o teste cria)
`raw_eventos(id, valor, carregado_em)` — com `id=1` aparecendo duas vezes (100 em 10/08 e 150 em 12/08).

## Tarefa
Em [`exercicio-03/solucao.sql`](exercicio-03/solucao.sql), devolva `(id, valor)` da versão mais
recente de cada `id`, ordenado por `id`.

```bash
cd ambiente && docker compose up -d
pip install psycopg2-binary pytest
pytest -q modulos/08-ingestao-integracao/exercicio-03
```

## Dicas progressivas
:::{dropdown} Dica 1 — numere as versões
`ROW_NUMBER() OVER (PARTITION BY id ORDER BY carregado_em DESC) AS rn`.
:::
:::{dropdown} Dica 2 — fique com a mais nova
Envolva num subselect e filtre `WHERE rn = 1`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
SELECT id, valor
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY carregado_em DESC) AS rn
  FROM raw_eventos
) t
WHERE rn = 1
ORDER BY id;
```
`ROW_NUMBER` ordena as versões de cada `id` (mais nova = 1); `rn = 1` mantém só ela. É o padrão
para lidar com arquivos reentregues sem inflar os dados a jusante.
:::

---
**Revisado em:** 2026-08-29
