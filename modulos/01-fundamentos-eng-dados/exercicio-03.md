# Exercicio 03 - Ordenar o ciclo de vida do dado (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`ordena_ciclo_vida`** - Dada uma lista de etapas fora de ordem, retorne-as na ordem canonica do ciclo de vida: geracao, ingestao, armazenamento, transformacao, disponibilizacao (so as presentes).

```bash
cd modulos/01-fundamentos-eng-dados/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
filtre a ordem canonica pelas etapas presentes.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def ordena_ciclo_vida(etapas):
    ordem = ['geracao', 'ingestao', 'armazenamento', 'transformacao', 'disponibilizacao']
    return [e for e in ordem if e in etapas]
```
:::

---
**Revisado em:** 2026-08-31
