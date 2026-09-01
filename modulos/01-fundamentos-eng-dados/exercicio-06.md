# Exercicio 06 - Armazenamento ideal por carga (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`armazenamento_ideal`** - OLTP favorece armazenamento por 'linha' (row); OLAP favorece por 'coluna' (colunar). Retorne 'linha' p/ 'OLTP', 'coluna' p/ 'OLAP', senao 'indefinido'.

```bash
cd modulos/01-fundamentos-eng-dados/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
OLTP->linha, OLAP->coluna.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def armazenamento_ideal(carga):
    if carga == 'OLTP':
        return 'linha'
    if carga == 'OLAP':
        return 'coluna'
    return 'indefinido'
```
:::

---
**Revisado em:** 2026-08-31
