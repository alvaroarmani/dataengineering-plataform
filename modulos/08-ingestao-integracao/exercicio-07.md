# Exercício 07 — Validar contra um schema (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Formatos com **schema** (Avro, Parquet) rejeitam dados fora do tipo. Implemente essa validação.

## Tarefa
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py):

- **`valida_registro(registro, schema)`** — `schema` = `{campo: tipo}`. Retorne a lista
  **ordenada** dos campos com problema (**ausentes** ou de **tipo errado**). Válido → `[]`.

```bash
cd modulos/08-ingestao-integracao/exercicio-07
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — percorra o schema
Para cada `campo, tipo` do schema: se `campo not in registro` **ou** `not isinstance(registro[campo], tipo)` → problema.
:::
:::{dropdown} Dica 2 — ordenado
Colete numa lista e `return sorted(problemas)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def valida_registro(registro, schema):
    problemas = []
    for campo, tipo in schema.items():
        if campo not in registro or not isinstance(registro[campo], tipo):
            problemas.append(campo)
    return sorted(problemas)
```
É o que um formato com schema faz na escrita (schema-on-write): garante tipos e presença dos
campos. O Avro leva isso adiante com **evolução de schema** (campos novos opcionais sem quebrar
consumidores antigos).
:::

---
**Revisado em:** 2026-08-29
