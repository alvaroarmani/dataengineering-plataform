# Exercício 05 — Janela tumbling por tempo de evento (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`janela_tumbling`** — Agregação por tempo de evento em janelas fixas (tumbling). Dado o timestamp do evento (em segundos) e o tamanho da janela, retorne o INÍCIO da janela a que ele pertence.

```bash
cd modulos/17-streaming-tempo-real/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
arredonde para baixo ao múltiplo do tamanho: (event_ts // tamanho) * tamanho.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def janela_tumbling(event_ts, tamanho_seg):
    return (event_ts // tamanho_seg) * tamanho_seg
```
:::

---
**Revisado em:** 2026-08-31
