# Exercício 07 — Deve alertar? (severidade) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py): implemente **`deve_alertar`** — checks = lista de (nome, status) com status em {'pass','warn','fail'}. True se houver algum 'fail'.

```bash
cd modulos/12-qualidade-observabilidade/exercicio-07
pytest -q
```

## Dica
:::{dropdown} Dica
any(status == 'fail' ...).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def deve_alertar(checks):
    return any(status == 'fail' for _, status in checks)
```
:::

---
**Revisado em:** 2026-08-29
