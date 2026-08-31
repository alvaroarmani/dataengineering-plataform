# Exercício 06 — Balanceamento: nó de menor carga (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`menor_carga`** — nos = {no: carga}. Para colocar o próximo shard, retorne o nó de MENOR carga; em empate, o de menor nome (ordem alfabética).

```bash
cd modulos/19-sistemas-distribuidos/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
min por (carga, nome) resolve o empate pelo nome.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def menor_carga(nos):
    return min(nos, key=lambda k: (nos[k], k))
```
:::

---
**Revisado em:** 2026-08-31
