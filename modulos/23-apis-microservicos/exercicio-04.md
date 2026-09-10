# Exercicio 04 - Retry com backoff exponencial (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`backoff`** - Ao falhar, um consumidor espera mais a cada tentativa (backoff exponencial). Retorne o tempo de espera = base * 2**(tentativa-1) (tentativa comeca em 1).

```bash
cd modulos/23-apis-microservicos/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
espera = base * 2**(tentativa-1): 1a=base, 2a=2*base, 3a=4*base...
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def backoff(tentativa, base):
    return base * (2 ** (tentativa - 1))
```
:::

---
**Revisado em:** 2026-09-09
