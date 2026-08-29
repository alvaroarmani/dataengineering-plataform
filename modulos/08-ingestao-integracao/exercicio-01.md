# Exercício 01 — Upsert idempotente (TRACK REAL · Postgres)

**Onde roda:** 🐳 Bancada Docker (Postgres real). Sem bancada? Faça o [Exercício 02](exercicio-02.md)
(a lógica do incremental, no navegador).

Você recebe um **lote incremental** (`batch`) e precisa integrá-lo ao destino (`clientes`) de
forma **idempotente** — rodar duas vezes não pode duplicar.

## Tabelas (o teste cria)
- `clientes(id PK, nome)` — destino, já com `(1,'ana'),(2,'bruno')`.
- `batch(id, nome)` — lote que chegou: `(2,'bruno silva')` [update], `(3,'caio')` [novo].

## Tarefa
Escreva em [`exercicio-01/solucao.sql`](exercicio-01/solucao.sql) um **UPSERT** de `batch`
para `clientes` (insere novos, atualiza existentes por `id`).

```bash
cd ambiente && docker compose up -d
pip install psycopg2-binary pytest
pytest -q modulos/08-ingestao-integracao/exercicio-01
```
✅ O grader roda sua solução **duas vezes** e confere que o resultado é
`(1,ana),(2,bruno silva),(3,caio)` **sem duplicatas** — ou seja, idempotente.

## Dicas progressivas
:::{dropdown} Dica 1 — o padrão
`INSERT INTO clientes (id, nome) SELECT id, nome FROM batch ON CONFLICT (id) DO UPDATE SET ...`.
:::
:::{dropdown} Dica 2 — o SET
Use `EXCLUDED` (a linha que tentou entrar): `DO UPDATE SET nome = EXCLUDED.nome`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
INSERT INTO clientes (id, nome)
SELECT id, nome FROM batch
ON CONFLICT (id) DO UPDATE SET nome = EXCLUDED.nome;
```
`ON CONFLICT (id)` detecta a chave que já existe e faz `UPDATE` em vez de inserir duplicata;
`EXCLUDED.nome` é o valor do lote. Por isso reexecutar converge para o mesmo estado —
**idempotência**, o que torna um retry seguro.
:::

---
**Revisado em:** 2026-08-29
