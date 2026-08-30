# Exercício 08 — Consumo por offset (Kafka) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

No Kafka, um consumidor lê de um **offset** e avança, committando até onde leu. Implemente essa
mecânica.

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py):

- **`consumir(log, offset)`** — `log` é a lista de mensagens; `offset` é o índice da próxima a
  ler. Retorne `(novas_mensagens, novo_offset)`: as mensagens a partir de `offset` e o offset atualizado.

```bash
cd modulos/08-ingestao-integracao/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — as novas
`novas = log[offset:]` (do offset até o fim).
:::
:::{dropdown} Dica 2 — o novo offset
Avança para `len(log)` (leu tudo o que havia).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def consumir(log, offset):
    novas = log[offset:]
    return novas, offset + len(novas)
```
Guardando (committando) o `novo_offset`, o consumidor **retoma de onde parou** — sem
reprocessar nem perder mensagens. É a base do "ao menos uma vez / exatamente uma vez" no Kafka.
:::

---
**Revisado em:** 2026-08-29
