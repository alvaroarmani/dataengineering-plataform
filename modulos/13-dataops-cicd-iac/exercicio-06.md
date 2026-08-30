# Exercício 06 — Quantas mudanças o apply faria (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`num_mudancas`** — Nº total de mudanças (criar + atualizar + destruir) entre atual e desejado.

```bash
cd modulos/13-dataops-cicd-iac/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
some create+update+destroy do diff.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def num_mudancas(atual, desejado):
    criar = sum(1 for k in desejado if k not in atual)
    destruir = sum(1 for k in atual if k not in desejado)
    atualizar = sum(1 for k in desejado if k in atual and desejado[k] != atual[k])
    return criar + atualizar + destruir
```
:::

---
**Revisado em:** 2026-08-29
