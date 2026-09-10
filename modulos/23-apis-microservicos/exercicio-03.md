# Exercicio 03 - Idempotency-Key (nao reprocessar) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`deve_processar`** - APIs usam uma Idempotency-Key para nao processar a mesma requisicao 2x. Retorne True se `chave` ainda NAO foi processada (nao esta em `processados`).

```bash
cd modulos/23-apis-microservicos/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
processe so se a chave for nova: chave not in processados.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def deve_processar(processados, chave):
    return chave not in processados
```
:::

---
**Revisado em:** 2026-09-09
