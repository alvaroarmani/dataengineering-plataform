# Exercício 05 — Achatar JSON de uma API (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Ingerir de API = receber JSON **aninhado** e transformá-lo numa tabela plana. Aqui você
implementa exatamente esse passo.

## Tarefa

Implemente, em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), a função
`achatar_pedidos(payload)` que recebe um dicionário no formato:

```python
{"pedidos": [
    {"id": 1, "cliente": {"nome": "ana"}, "itens": [{"valor": 50}, {"valor": 30}]},
    ...
]}
```

e retorna uma **lista de dicts planos**, um por pedido, na ordem de entrada, com as chaves:
- **`id`** — o id do pedido;
- **`cliente`** — o nome do cliente (de `cliente.nome`);
- **`total`** — a **soma** dos `valor` dos `itens` (0.0 se não houver itens).

```bash
cd modulos/03-python-eng-dados/exercicio-05
pytest -q
```

Exemplo:
```python
achatar_pedidos({"pedidos": [
    {"id": 1, "cliente": {"nome": "ana"}, "itens": [{"valor": 50}, {"valor": 30}]},
]})
# -> [{"id": 1, "cliente": "ana", "total": 80.0}]
```

## Dicas progressivas
:::{dropdown} Dica 1 — percorra os pedidos
Itere `payload["pedidos"]` e monte um dict por pedido.
:::
:::{dropdown} Dica 2 — navegar o aninhamento
O nome está em `p["cliente"]["nome"]`; o total é `sum(item["valor"] for item in p["itens"])`.
:::
:::{dropdown} Dica 3 — sem itens
Use `p.get("itens", [])` para o `sum` dar 0.0 quando não houver itens (some com `0.0` inicial).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def achatar_pedidos(payload):
    linhas = []
    for p in payload.get("pedidos", []):
        total = sum((item["valor"] for item in p.get("itens", [])), 0.0)
        linhas.append({
            "id": p["id"],
            "cliente": p["cliente"]["nome"],
            "total": total,
        })
    return linhas
```
Navegamos o JSON aninhado (`p["cliente"]["nome"]`) e agregamos os itens com `sum(..., 0.0)`
— o `0.0` inicial garante `float` e trata a lista vazia. É o mesmo gesto de toda ingestão
de API: do JSON hierárquico para linhas planas prontas para virar tabela.
:::

---
**Revisado em:** 2026-08-22
