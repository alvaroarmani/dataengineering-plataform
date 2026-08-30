# Exercício 08 — Schema enforcement (aceitar escrita?) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py): implemente **`aceita_escrita`** — schema = {campo: nome_do_tipo} (ex.: {'id':'int','nome':'str'}). True se o registro tiver TODOS os campos com o tipo certo; senão False.

```bash
cd modulos/11-spark-lakehouse/exercicio-08
pytest -q
```

## Dica
:::{dropdown} Dica
Compare `type(registro[c]).__name__` com o nome do tipo esperado, para todos os campos.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def aceita_escrita(schema, registro):
    return all(c in registro and type(registro[c]).__name__ == t for c, t in schema.items())
```
:::

---
**Revisado em:** 2026-08-29
