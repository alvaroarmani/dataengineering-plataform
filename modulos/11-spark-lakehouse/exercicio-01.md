# Exercício 01 — Transformação (lazy) vs ação (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`eh_acao`** — True para ações (count/collect/show/write/take/first); False para transformações.

```bash
cd modulos/11-spark-lakehouse/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
Compare `op` com o conjunto de ações.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def eh_acao(op):
    acoes = {'count','collect','show','write','take','first','save'}
    return op in acoes
```
:::

---
**Revisado em:** 2026-08-29
