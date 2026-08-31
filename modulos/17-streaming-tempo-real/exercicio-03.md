# Exercício 03 — Partição de uma chave (Kafka) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`particao`** — Kafka manda a mesma chave sempre para a mesma partição. Implemente com hash simples e estável: soma dos códigos dos caracteres da chave, módulo o número de partições.

```bash
cd modulos/17-streaming-tempo-real/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
sum(ord(c) for c in str(chave)) % num_particoes — determinístico: mesma chave, mesma partição.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def particao(chave, num_particoes):
    return sum(ord(c) for c in str(chave)) % num_particoes
```
:::

---
**Revisado em:** 2026-08-31
