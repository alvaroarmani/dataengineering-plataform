# Exercício 03 — Rodar pipeline (para na 1ª falha) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`rodar_pipeline`** — etapas = lista de (nome, ok). Rode em ordem; pare na 1ª que falhar. Retorne (passou, etapa_que_falhou_ou_None).

```bash
cd modulos/13-dataops-cicd-iac/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
itere; no 1º ok False, retorne (False, nome).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def rodar_pipeline(etapas):
    for nome, ok in etapas:
        if not ok:
            return (False, nome)
    return (True, None)
```
:::

---
**Revisado em:** 2026-08-29
