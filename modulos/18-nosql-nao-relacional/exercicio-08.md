# Exercicio 08 - Ranquear por frequencia (TF) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py): implemente **`ranquear`** - docs = lista de (doc_id, texto). Retorne os doc_ids que contem `termo`, ORDENADOS por frequencia do termo (maior primeiro); empate pelo doc_id (menor primeiro).

```bash
cd modulos/18-nosql-nao-relacional/exercicio-08
pytest -q
```

## Dica
:::{dropdown} Dica
conte a frequencia do termo em cada doc; filtre >0; ordene por (-frequencia, doc_id).
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def ranquear(docs, termo):
    pontuados = [(doc_id, texto.lower().split().count(termo)) for doc_id, texto in docs]
    pontuados = [(d, s) for d, s in pontuados if s > 0]
    pontuados.sort(key=lambda x: (-x[1], x[0]))
    return [d for d, _ in pontuados]
```
:::

---
**Revisado em:** 2026-09-09
