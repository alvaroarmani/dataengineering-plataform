# Exercício 01 — Top categorias por receita (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Agregar e **ranquear** é o feijão com arroz da análise. Aqui você combina `dict` (agregação)
com `sorted` (ordenação) e `tuple` (registro do resultado).

## Tarefa

Implemente, em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), a função
`top_n_categorias(pedidos, n)` que recebe uma lista de dicts `{"categoria": str, "valor": float}`
e retorna as **`n` categorias de maior receita**, como uma **lista de tuplas**
`(categoria, receita_total)` em ordem **decrescente de receita**. Em caso de empate na
receita, ordene por **categoria em ordem alfabética**.

```bash
cd modulos/03-python-eng-dados/exercicio-01
pytest -q
```

Exemplo:
```python
top_n_categorias([
    {"categoria": "livros", "valor": 50},
    {"categoria": "eletronicos", "valor": 1200},
    {"categoria": "livros", "valor": 30},
], n=2)
# -> [("eletronicos", 1200.0), ("livros", 80.0)]
```

## Dicas progressivas
:::{dropdown} Dica 1 — agregue primeiro
Some a receita por categoria num `dict` (com `.get`), como no lab.
:::
:::{dropdown} Dica 2 — ordene e corte
`sorted(itens, key=...)` com uma chave que ordene por receita desc e categoria asc; depois pegue os `n` primeiros com fatiamento `[:n]`.
:::
:::{dropdown} Dica 3 — a chave de ordenação
`key=lambda kv: (-kv[1], kv[0])` ordena por receita decrescente e, no empate, por nome crescente.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def top_n_categorias(pedidos, n):
    receita = {}
    for p in pedidos:
        c = p["categoria"]
        receita[c] = receita.get(c, 0.0) + p["valor"]
    ordenado = sorted(receita.items(), key=lambda kv: (-kv[1], kv[0]))
    return ordenado[:n]
```
`receita.items()` dá pares `(categoria, total)`; a chave `(-total, categoria)` resolve
ordem e desempate de uma vez; o fatiamento `[:n]` pega o topo. Note que os valores viram
`float` por causa do acumulador `0.0`.
:::

---
**Revisado em:** 2026-08-21
