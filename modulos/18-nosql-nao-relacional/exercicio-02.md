# Exercício 02 — Agregação em documentos (contar por campo) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`contar_por`** — docs = lista de dicts (documentos). Retorne {valor: contagem} agrupando pelo `campo` (estilo agregação de banco documento).

```bash
cd modulos/18-nosql-nao-relacional/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
itere os docs; acumule a contagem de d.get(campo) num dict.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def contar_por(docs, campo):
    r = {}
    for d in docs:
        k = d.get(campo)
        r[k] = r.get(k, 0) + 1
    return r
```
:::

---
**Revisado em:** 2026-08-31
