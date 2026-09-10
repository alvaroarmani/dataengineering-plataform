# Exercicio 10 - Contar stages (shuffle boundaries) (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Aplica a [teoria 05](teoria-05-spark-avancado-execucao-skew.md).

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py): implemente **`contar_stages`** - No Spark, cada transformacao WIDE gera um shuffle e fecha/abre um stage. transformacoes = lista de (nome, tipo) com tipo 'narrow' ou 'wide'. Retorne o numero de stages = (numero de wide) + 1.

```bash
cd modulos/11-spark-lakehouse/exercicio-10
pytest -q
```

## Dica
:::{dropdown} Dica
conte as transformacoes wide (shuffles) e some 1 (o stage inicial).
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def contar_stages(transformacoes):
    wides = sum(1 for _, tipo in transformacoes if tipo == 'wide')
    return wides + 1
```
:::

---
**Revisado em:** 2026-09-09
