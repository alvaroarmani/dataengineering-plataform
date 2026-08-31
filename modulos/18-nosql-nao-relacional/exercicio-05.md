# Exercício 05 — Downsample de série temporal (buckets) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`downsample_soma`** — pontos = lista de (timestamp_seg, valor). Agregue por janelas fixas de `bucket_seg` somando os valores. Retorne {inicio_do_bucket: soma}.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
bucket = (ts // bucket_seg) * bucket_seg; some os valores por bucket.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def downsample_soma(pontos, bucket_seg):
    r = {}
    for ts, valor in pontos:
        b = (ts // bucket_seg) * bucket_seg
        r[b] = r.get(b, 0) + valor
    return r
```
:::

---
**Revisado em:** 2026-08-31
