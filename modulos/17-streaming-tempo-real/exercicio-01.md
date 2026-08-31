# Exercício 01 — Roteamento de eventos (fan-out) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`roteia`** — assinaturas = {consumidor: [tipos que assina]}. Retorne a lista ORDENADA de consumidores que assinam `evento_tipo` (event-driven: publique uma vez, muitos consomem).

```bash
cd modulos/17-streaming-tempo-real/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
filtre os consumidores cujo conjunto de tipos contém evento_tipo; ordene.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def roteia(evento_tipo, assinaturas):
    return sorted(c for c, tipos in assinaturas.items() if evento_tipo in tipos)
```
:::

---
**Revisado em:** 2026-08-31
