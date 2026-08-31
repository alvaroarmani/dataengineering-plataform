# Exercício 02 — Classificar latência (batch vs streaming) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`classifica_latencia`** — Retorne 'tempo-real' se a latência exigida for < 1s; 'quase-real' se < 60s; senão 'batch' (a solução mais simples).

```bash
cd modulos/17-streaming-tempo-real/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
dois cortes: < 1s e < 60s; acima disso, batch.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def classifica_latencia(latencia_seg):
    if latencia_seg < 1:
        return 'tempo-real'
    if latencia_seg < 60:
        return 'quase-real'
    return 'batch'
```
:::

---
**Revisado em:** 2026-08-31
