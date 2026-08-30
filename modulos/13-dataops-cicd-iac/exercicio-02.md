# Exercício 02 — Ambiente do branch (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`ambiente_do_branch`** — main -> 'prod'; develop -> 'staging'; começa com 'feature/' -> 'dev'; senão 'nenhum'.

```bash
cd modulos/13-dataops-cicd-iac/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
mapeie main/develop/feature/* para prod/staging/dev.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def ambiente_do_branch(branch):
    if branch == 'main':
        return 'prod'
    if branch == 'develop':
        return 'staging'
    if branch.startswith('feature/'):
        return 'dev'
    return 'nenhum'
```
:::

---
**Revisado em:** 2026-08-29
