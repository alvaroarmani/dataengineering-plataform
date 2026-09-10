# Exercicio 07 - Agregacao em fluxo (single-pass) (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Exercicio **complexo** que aplica a [teoria 07](teoria-07-python-avancado-dados.md).

## Tarefa
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py): implemente **`agrega_stream`** - Agregue um FLUXO de eventos numa unica passada (funciona em qualquer iteravel/generator, sem carregar tudo). eventos = iteravel de (chave, valor). Retorne {chave: (n, soma, maximo)} por chave.

```bash
cd modulos/03-python-eng-dados/exercicio-07
pytest -q
```

## Dica
:::{dropdown} Dica
acumule n/soma/max por chave numa passada; nao use len/index (pense em iterador).
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def agrega_stream(eventos):
    res = {}
    for chave, valor in eventos:
        if chave not in res:
            res[chave] = [0, 0, valor]
        r = res[chave]
        r[0] += 1
        r[1] += valor
        r[2] = max(r[2], valor)
    return {k: tuple(v) for k, v in res.items()}
```
:::

---
**Revisado em:** 2026-09-09
