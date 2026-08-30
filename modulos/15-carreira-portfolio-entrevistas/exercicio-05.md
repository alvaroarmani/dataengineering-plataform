# Exercício 05 — Batch ou streaming? (system design) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`escolher_processamento`** — Dada a latência exigida em segundos, retorne 'streaming' se for menor que 60; caso contrário 'batch' (a solução mais simples que atende).

```bash
cd modulos/15-carreira-portfolio-entrevistas/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
latência baixa (<60s) exige streaming; janelas maiores → batch.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def escolher_processamento(latencia_seg):
    return 'streaming' if latencia_seg < 60 else 'batch'
```
:::

---
**Revisado em:** 2026-08-30
