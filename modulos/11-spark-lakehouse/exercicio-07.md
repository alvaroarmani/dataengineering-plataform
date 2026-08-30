# Exercício 07 — Time travel: arquivos de uma versão (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py): implemente **`arquivos_da_versao`** — cada versão do log é o conjunto de arquivos daquele snapshot.

```bash
cd modulos/11-spark-lakehouse/exercicio-07
pytest -q
```

## Dica
:::{dropdown} Dica
Retorne sorted(log[versao]).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def arquivos_da_versao(log, versao):
    return sorted(log[versao])
```
:::

---
**Revisado em:** 2026-08-29
