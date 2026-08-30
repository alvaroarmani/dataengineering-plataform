# Exercício 02 — Quando o Spark executa (lazy) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`primeira_acao`** — as transformações antes só montam o plano; a 1ª ação dispara tudo.

```bash
cd modulos/11-spark-lakehouse/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
Ache o 1º índice cujo op é uma ação.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def primeira_acao(ops):
    acoes = {'count','collect','show','write','take','first','save'}
    for i, op in enumerate(ops):
        if op in acoes:
            return i
    return -1
```
:::

---
**Revisado em:** 2026-08-29
