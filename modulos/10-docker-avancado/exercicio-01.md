# Exercício 01 — Cache de camadas do Docker (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`camadas_reconstruidas`** — a partir do 1º passo alterado, todas as camadas seguintes rebuildam (o cache é invalidado dali pra baixo).

```bash
cd modulos/10-docker-avancado/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
`return list(passos[alterado_idx:])` — o cache vale só até o passo anterior.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def camadas_reconstruidas(passos, alterado_idx):
    return list(passos[alterado_idx:])
```
:::

---
**Revisado em:** 2026-08-29
