# Exercício 01 — Uma API REST de pedidos: o status code certo, na ordem certa

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Saber que `404` é "não encontrado" é fácil. O difícil — e o que separa uma API boa de uma que
confunde quem a consome — é decidir **qual erro vence** quando vários se aplicam, e garantir que um
erro **nunca** altere o estado. Você vai escrever o núcleo de um endpoint `/pedidos`, do tipo que
serve os dados do seu pipeline para um app (teoria 01, "Servir dados").

Além dos códigos da teoria (`200`, `201`, `204`, `400`, `401`, `404`), use três que toda API séria
precisa:

| Código | Quando | Por que não outro |
|---|---|---|
| `403` Forbidden | sei quem você é, mas você não pode fazer isso | `401` é "não sei quem você é" |
| `405` Method Not Allowed | a rota existe, o método não (ex.: `DELETE /pedidos`) | `404` diria que a rota não existe |
| `409` Conflict | criar algo que já existe | `400` diria que o corpo está malformado — e não está |

A ordem das checagens **também é contrato**: autenticação primeiro (não revele a quem não se
identificou quais recursos existem), depois rota, método, permissão, existência e, por fim, o corpo.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente **`tratar(req, estado)`**
seguindo a ordem da docstring.

```bash
cd modulos/23-apis-microservicos/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — quebre o caminho
`partes = caminho.strip("/").split("/")`: `["pedidos"]` é a coleção; `["pedidos", "p1"]` é um item;
qualquer outra coisa é `404`. Guarde `colecao = len(partes) == 1`.
:::
:::{dropdown} Dica 2 — uma checagem por vez, com return
Escreva as checagens como uma sequência de `if ...: return status, {"erro": ...}` na ordem da
docstring. O código fica linear e a precedência fica visível. Para o escopo, um dict
`{"GET": "ler", "POST": "escrever", ...}` resolve.
:::
:::{dropdown} Dica 3 — validar o corpo
Cuidado com duas pegadinhas do Python: `True` é um `int` (exclua `bool` explicitamente) e `""` é uma
string válida (exija não vazia). Grave `dict(corpo)` — uma cópia — para que quem chamou não consiga
alterar o estado depois.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
ESCOPO = {"GET": "ler", "POST": "escrever", "PUT": "escrever", "DELETE": "escrever"}

def _corpo_valido(corpo):
    return (isinstance(corpo, dict) and isinstance(corpo.get("id"), str) and corpo["id"]
            and isinstance(corpo.get("valor"), (int, float))
            and not isinstance(corpo.get("valor"), bool) and corpo["valor"] > 0)

def tratar(req, estado):
    metodo, caminho = req.get("metodo"), req.get("caminho", "")
    token = estado["tokens"].get(req.get("token"))
    if token is None:
        return 401, {"erro": "não autenticado"}                     # 1
    partes = caminho.strip("/").split("/")
    if partes[0] != "pedidos" or len(partes) > 2 or (len(partes) == 2 and not partes[1]):
        return 404, {"erro": "rota inexistente"}                    # 2
    colecao = len(partes) == 1
    if metodo not in ({"GET", "POST"} if colecao else {"GET", "PUT", "DELETE"}):
        return 405, {"erro": "método não permitido"}                # 3
    if ESCOPO[metodo] not in token["escopos"]:
        return 403, {"erro": "sem permissão"}                       # 4
    pedidos = estado["pedidos"]
    if colecao:
        if metodo == "GET":
            return 200, {"pedidos": [pedidos[k] for k in sorted(pedidos)]}
        corpo = req.get("corpo")
        if not _corpo_valido(corpo):
            return 400, {"erro": "corpo inválido"}                  # 6
        if corpo["id"] in pedidos:
            return 409, {"erro": "pedido já existe"}                # 7
        pedidos[corpo["id"]] = dict(corpo)
        return 201, dict(corpo)
    pid = partes[1]
    if pid not in pedidos:
        return 404, {"erro": "pedido inexistente"}                  # 5
    if metodo == "GET":
        return 200, dict(pedidos[pid])
    if metodo == "DELETE":
        del pedidos[pid]
        return 204, None
    corpo = req.get("corpo")
    if not _corpo_valido(corpo) or corpo["id"] != pid:
        return 400, {"erro": "corpo inválido"}                      # 6
    pedidos[pid] = dict(corpo)
    return 200, dict(corpo)
```
**Ligação com o resto do curso:** do lado de quem **consome** a API (M08), essa tabela vira lógica
de resiliência — `4xx` não se repete (conserte a requisição), `5xx` e `429` sim, com backoff. E
repare que `PUT` e `DELETE` são **idempotentes** (repetir dá o mesmo estado), `POST` não — por isso
o `409`: ele impede que um retry do cliente crie o pedido duas vezes.
:::

---
**Revisado em:** 2026-09-29
