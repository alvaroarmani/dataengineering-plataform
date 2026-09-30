# Exercício 01 — Do relacional ao documento: desnormalizar e pagar o preço

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro — no lab 01 você faz o mesmo no MongoDB real).

## Contexto
A regra de ouro do modelo de documento (teoria 01) é **"o modelo segue a consulta"**: se a tela
principal mostra o pedido com o cliente e os itens, guarde tudo **num documento só** — uma leitura,
sem JOIN.

Só que isso tem preço. O nome e a cidade do cliente passam a existir em **N cópias**, uma por
pedido. Quando o cliente muda de cidade, você paga **N escritas** — e, se esquecer uma, os
documentos passam a discordar entre si. É o trade-off central da desnormalização:
**leitura barata ↔ escrita cara e risco de inconsistência**.

Neste exercício você vai construir os documentos a partir de tabelas relacionais e **medir** esse
custo.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente:

1. **`montar_documentos(clientes, pedidos, itens)`** — um documento por pedido, com cliente e itens
   embutidos, `total` calculado e integridade referencial verificada.
2. **`pedidos_do_cliente(docs, cliente_id)`** — os `_id` de um cliente.
3. **`atualizar_cidade(docs, cliente_id, nova_cidade)`** — atualiza todas as cópias e devolve
   **quantas escritas** isso custou.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — índices em dict antes de montar
Monte `por_cliente = {c["id"]: c for c in clientes}` e `por_pedido = {p["id"]: [] for p in pedidos}`.
Ao distribuir os itens, um `pedido_id` fora de `por_pedido` é um órfão → `ValueError`.
:::
:::{dropdown} Dica 2 — cópia, não referência
Se você fizer `"cliente": c`, todos os pedidos da Ana apontam para **o mesmo** dict — mudar um muda
todos (e muda a entrada). Crie um dict novo: `{"id": c["id"], "nome": c["nome"], "cidade": c["cidade"]}`.
:::
:::{dropdown} Dica 3 — contar escritas
Em `atualizar_cidade`, só conte (e só altere) quando o documento é do cliente **e** a cidade é
diferente. Assim, repetir a mesma atualização custa zero — idempotência.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def montar_documentos(clientes, pedidos, itens):
    por_cliente = {c["id"]: c for c in clientes}
    por_pedido = {p["id"]: [] for p in pedidos}
    for it in itens:
        if it["pedido_id"] not in por_pedido:
            raise ValueError(f"item órfão: pedido {it['pedido_id']}")
        por_pedido[it["pedido_id"]].append(
            {"produto": it["produto"], "qtd": it["qtd"], "preco": it["preco"]})
    docs = []
    for p in sorted(pedidos, key=lambda p: p["id"]):
        c = por_cliente.get(p["cliente_id"])
        if c is None:
            raise ValueError(f"cliente inexistente: {p['cliente_id']}")
        its = por_pedido[p["id"]]
        docs.append({
            "_id": p["id"], "data": p["data"],
            "cliente": {"id": c["id"], "nome": c["nome"], "cidade": c["cidade"]},  # cópia
            "itens": its,
            "total": round(sum(i["qtd"] * i["preco"] for i in its), 2),
        })
    return docs

def pedidos_do_cliente(docs, cliente_id):
    return sorted(d["_id"] for d in docs if d["cliente"]["id"] == cliente_id)

def atualizar_cidade(docs, cliente_id, nova_cidade):
    n = 0
    for d in docs:
        if d["cliente"]["id"] == cliente_id and d["cliente"]["cidade"] != nova_cidade:
            d["cliente"]["cidade"] = nova_cidade
            n += 1
    return n
```
**Como decidir na vida real:** embuta o que é lido junto e muda pouco (itens do pedido — nunca mudam
depois da compra). Para o que muda com frequência e é compartilhado por muitos documentos, guarde
só a **referência** (`cliente_id`) ou uma cópia **de propósito congelada** — o endereço de entrega
*no momento da compra* é, na verdade, o dado certo a guardar no pedido.

Repare que `pedidos_do_cliente` precisou varrer **todos** os documentos: a consulta que não guiou o
modelo fica cara. No MongoDB, isso pede um índice em `cliente.id`.
:::

---
**Revisado em:** 2026-09-29
