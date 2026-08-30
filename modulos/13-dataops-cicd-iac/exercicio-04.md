# Exercício 04 — Deve deployar? (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`deve_deployar`** — True somente se branch == 'main' E testes_ok forem True.

```bash
cd modulos/13-dataops-cicd-iac/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
branch main e testes verdes.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def deve_deployar(branch, testes_ok):
    return branch == 'main' and testes_ok
```
:::

---
**Revisado em:** 2026-08-29
