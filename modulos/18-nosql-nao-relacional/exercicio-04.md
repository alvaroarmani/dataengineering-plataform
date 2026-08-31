# Exercício 04 — Chave de partição (wide-column) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`chave_particao`** — No modelo wide-column (Cassandra), a chave de partição é composta pelas colunas de particionamento. Retorne a TUPLA dos valores de `linha` nas colunas `cols`, nessa ordem.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
monte uma tupla com linha[c] para cada c em cols (a ordem importa).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def chave_particao(linha, cols):
    return tuple(linha[c] for c in cols)
```
:::

---
**Revisado em:** 2026-08-31
