# Exercício 06 — Carga idempotente de um dia em Python (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Mesma ideia do [Exercício 05](exercicio-05.md) (overwrite da partição), aqui no navegador.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py):

- **`carregar_dia(fato, dia, batch)`** — remova de `fato` as linhas de `dia`, adicione as do
  `batch` (marcadas com `dia`), e retorne ordenado por `(data, id)`. Outros dias permanecem.

```bash
cd modulos/09-orquestracao-airflow/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — remova o dia
`novo = [linha for linha in fato if linha[0] != dia]`.
:::
:::{dropdown} Dica 2 — some o batch e ordene
`novo += [(dia, i, v) for i, v in batch]`; depois `return sorted(novo)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def carregar_dia(fato, dia, batch):
    novo = [linha for linha in fato if linha[0] != dia]   # tira o dia antigo
    novo += [(dia, i, v) for i, v in batch]                # põe o dia novo
    return sorted(novo)
```
Reprocessar (rodar de novo com o mesmo batch) remove e recoloca as mesmas linhas — converge
para o mesmo estado, **idempotente**. É a versão em memória do `DELETE + INSERT` do Exercício 05.
:::

---
**Revisado em:** 2026-08-29
