# Exercício 04 — Dedup de reentrega em Python (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Mesma lógica do [Exercício 03](exercicio-03.md) (dedup no Postgres), aqui no navegador.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py):

- **`dedup(linhas)`** — dado `linhas` = lista de `(id, valor, carregado_em)`, retorne a lista de
  `(id, valor)` da versão **mais recente** (maior `carregado_em`) de cada `id`, **ordenada por id**.

```bash
cd modulos/08-ingestao-integracao/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — a mais recente por id
Percorra ordenando por `carregado_em` e vá guardando num dict `{id: valor}` — o último a entrar vence.
:::
:::{dropdown} Dica 2 — saída ordenada
`sorted(mapa.items())` devolve `(id, valor)` em ordem de id.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def dedup(linhas):
    mapa = {}
    for id_, valor, ts in sorted(linhas, key=lambda r: r[2]):
        mapa[id_] = valor          # o mais recente sobrescreve
    return sorted(mapa.items())
```
Ordenando por `carregado_em` crescente e sobrescrevendo o dict, a última escrita por `id` é a
mais recente — o mesmo efeito do `ROW_NUMBER ... rn=1` do Exercício 03.
:::

---
**Revisado em:** 2026-08-29
