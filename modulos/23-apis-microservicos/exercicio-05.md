# Exercicio 05 - Saga: compensacoes (rollback) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`compensacoes`** - Numa Saga, se algo falha, desfazem-se os passos ja concluidos na ORDEM INVERSA. Dada a lista de passos concluidos, retorne as compensacoes em ordem reversa. Mapa: reservar->liberar, cobrar->estornar, enviar->cancelar_envio.

```bash
cd modulos/23-apis-microservicos/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
para cada passo concluido, na ordem inversa, a acao compensatoria.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def compensacoes(passos_ok):
    comp = {'reservar': 'liberar', 'cobrar': 'estornar', 'enviar': 'cancelar_envio'}
    return [comp[p] for p in reversed(passos_ok)]
```
:::

---
**Revisado em:** 2026-09-09
