# Exercício 06 — Anomalia de volume (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`anomalia_volume`** — True se |atual - média(historico)| > tolerancia * média(historico) (variação relativa).

```bash
cd modulos/12-qualidade-observabilidade/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
compare o desvio do atual vs a média com tolerancia*média.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def anomalia_volume(historico, atual, tolerancia):
    media = sum(historico)/len(historico)
    return abs(atual - media) > tolerancia * media
```
:::

---
**Revisado em:** 2026-08-29
