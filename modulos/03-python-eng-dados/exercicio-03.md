# Exercício 03 — Quarentena de valores (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Ingerir dados sujos sem derrubar o lote é uma habilidade diária. Aqui você implementa o
padrão de **quarentena** com `try/except` e type hints.

## Tarefa

Implemente, em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), a função
`converter_valores(itens)` que recebe uma lista de strings e retorna uma **tupla**
`(validos, invalidos)`:

- `validos`: lista de `float` das strings que **puderam** ser convertidas (na ordem de entrada).
- `invalidos`: lista das strings **originais** que falharam na conversão (na ordem de entrada).

```bash
cd modulos/03-python-eng-dados/exercicio-03
pytest -q
```

Exemplo:
```python
converter_valores(["10", "x", "3.5", ""])
# -> ([10.0, 3.5], ["x", ""])
```

## Dicas progressivas
:::{dropdown} Dica 1 — duas listas
Crie `validos` e `invalidos` vazias e percorra `itens`.
:::
:::{dropdown} Dica 2 — try/except específico
Tente `float(item)`; capture **`ValueError`** e mande o item original para `invalidos`.
:::
:::{dropdown} Dica 3 — retorno
Retorne a tupla `(validos, invalidos)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def converter_valores(itens: list[str]) -> tuple[list[float], list[str]]:
    validos: list[float] = []
    invalidos: list[str] = []
    for item in itens:
        try:
            validos.append(float(item))
        except ValueError:
            invalidos.append(item)      # quarentena: guarda o original
    return validos, invalidos
```
Capturamos **apenas** `ValueError` (o erro esperado de `float("x")`) — um `except` pelado
esconderia bugs. Os inválidos guardam a string original para inspeção/log posterior; o lote
segue sem cair.
:::

---
**Revisado em:** 2026-08-21
