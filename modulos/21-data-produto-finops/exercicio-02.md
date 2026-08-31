# Exercício 02 — Economia com particionamento (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`economia_particao`** — Particionar faz a consulta ler só uma fração dos dados. Retorne a ECONOMIA em dinheiro vs varrer tudo: tb_total * (1 - fracao_lida) * preco_tb.

```bash
cd modulos/21-data-produto-finops/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
economia = bytes evitados * preço = total * (1 - fração) * preço.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def economia_particao(tb_total, fracao_lida, preco_tb):
    return tb_total * (1 - fracao_lida) * preco_tb
```
:::

---
**Revisado em:** 2026-08-31
