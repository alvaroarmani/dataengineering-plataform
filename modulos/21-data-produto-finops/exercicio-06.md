# Exercício 06 — Data product pronto? (o que falta) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`requisitos_faltando`** — Um data product precisa de: dono, SLA, documentação e qualidade. checklist = {requisito: bool}. Retorne a lista ORDENADA dos requisitos ainda não atendidos (valor False).

```bash
cd modulos/21-data-produto-finops/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
filtre as chaves com valor False e ordene.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def requisitos_faltando(checklist):
    return sorted(k for k, ok in checklist.items() if not ok)
```
:::

---
**Revisado em:** 2026-08-31
