# Exercicio 07 - Indice invertido (full-text) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py): implemente **`indice_invertido`** - docs = lista de (doc_id, texto). Construa um indice invertido {termo: [doc_ids ordenados]} — os termos sao as palavras do texto em minusculas (separadas por espaco), sem repetir doc_id por termo.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-07
pytest -q
```

## Dica
:::{dropdown} Dica
para cada doc, para cada termo unico, acumule o doc_id num set; no fim, ordene as listas.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def indice_invertido(docs):
    idx = {}
    for doc_id, texto in docs:
        for termo in set(texto.lower().split()):
            idx.setdefault(termo, set()).add(doc_id)
    return {t: sorted(ids) for t, ids in idx.items()}
```
:::

---
**Revisado em:** 2026-09-09
