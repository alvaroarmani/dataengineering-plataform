# Exercício 08 — Fora da faixa esperada (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py): implemente **`fora_da_faixa`** — True se `valor` estiver fora de [minimo, maximo] (anomalia por limiar).

```bash
cd modulos/12-qualidade-observabilidade/exercicio-08
pytest -q
```

## Dica
:::{dropdown} Dica
valor < minimo ou valor > maximo.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def fora_da_faixa(valor, minimo, maximo):
    return valor < minimo or valor > maximo
```
:::

---
**Revisado em:** 2026-08-29
