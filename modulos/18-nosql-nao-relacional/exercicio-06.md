# Exercício 06 — Quórum e consistência (CAP) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`leitura_consistente`** — Num sistema com N réplicas e quóruns de leitura R e escrita W, a leitura é fortemente consistente quando R + W > N. Retorne esse booleano.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
a regra do quórum: R + W > N garante interseção entre quem escreveu e quem lê.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def leitura_consistente(n, r, w):
    return r + w > n
```
:::

---
**Revisado em:** 2026-08-31
