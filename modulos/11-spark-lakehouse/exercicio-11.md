# Exercicio 11 - Detectar particoes com skew (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Aplica a [teoria 05](teoria-05-spark-avancado-execucao-skew.md).

## Tarefa
Em [`exercicio-11/solucao.py`](exercicio-11/solucao.py): implemente **`particoes_com_skew`** - Data skew: uma particao muito maior que a media trava o stage. tamanhos = lista de tamanhos das particoes; fator = limite. Retorne os INDICES (ordenados) das particoes cujo tamanho > fator * media.

```bash
cd modulos/11-spark-lakehouse/exercicio-11
pytest -q
```

## Dica
:::{dropdown} Dica
calcule a media; retorne os indices onde tamanho > fator*media (particoes skewed).
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def particoes_com_skew(tamanhos, fator):
    media = sum(tamanhos) / len(tamanhos)
    return [i for i, t in enumerate(tamanhos) if t > fator * media]
```
:::

---
**Revisado em:** 2026-09-09
