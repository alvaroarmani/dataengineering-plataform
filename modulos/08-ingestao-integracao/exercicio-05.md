# Exercício 05 — Paginação: baixar todas as páginas (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Toda API grande **pagina**. Implemente o laço que baixa **tudo** — a lógica por trás da
ingestão de API (Lab 03), sem depender de rede.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py):

- **`coletar_tudo(buscar_pagina)`** — `buscar_pagina(n)` devolve a lista da página `n` (começa em
  1) e uma **lista vazia** quando acaba. Retorne a concatenação de **todos** os itens, na ordem.

```bash
cd modulos/08-ingestao-integracao/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — o laço
Comece em `n = 1`, busque a página, **pare quando vier vazia**, senão acumule e `n += 1`.
:::
:::{dropdown} Dica 2 — acumular
`itens.extend(pagina)` a cada página não-vazia.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def coletar_tudo(buscar_pagina):
    itens, n = [], 1
    while True:
        pagina = buscar_pagina(n)
        if not pagina:
            break
        itens.extend(pagina)
        n += 1
    return itens
```
Esse é o coração da ingestão de API: pagina até esgotar. Na vida real, `buscar_pagina` faz o
`GET` (com timeout e retry) e você escreveria cada página de forma idempotente (upsert).
:::

---
**Revisado em:** 2026-08-29
