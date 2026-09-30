"""Exercício 01 (M23) — Uma API REST de pedidos: o status code certo, na ordem certa.

Rode `pytest -q`.

Requisição:  {"metodo": "GET"|"POST"|"PUT"|"DELETE", "caminho": "/pedidos" ou "/pedidos/<id>",
              "token": str ou None, "corpo": dict ou None}
Estado:      {"pedidos": {id: {"id": id, "valor": número}},
              "tokens":  {token: {"escopos": {"ler", "escrever"}}}}
"""


def tratar(req: dict, estado: dict) -> tuple:
    """Processe a requisição, alterando `estado["pedidos"]` quando for o caso, e retorne
    (status, corpo_da_resposta). Verifique NESTA ORDEM — a primeira falha decide o status:

      1. token ausente ou desconhecido                            -> 401 {"erro": ...}
      2. caminho que não é /pedidos nem /pedidos/<id>             -> 404 {"erro": ...}
      3. método não aceito pela rota                              -> 405 {"erro": ...}
            /pedidos aceita GET e POST;  /pedidos/<id> aceita GET, PUT e DELETE
      4. escopo insuficiente (GET exige "ler"; POST/PUT/DELETE exigem "escrever") -> 403 {"erro": ...}
      5. /pedidos/<id> com id inexistente                         -> 404 {"erro": ...}
      6. corpo inválido em POST/PUT                               -> 400 {"erro": ...}
            válido = dict com "id" (str não vazia) e "valor" (número > 0, bool não vale);
            no PUT, o "id" do corpo tem de ser igual ao da URL
      7. POST de id que já existe                                 -> 409 {"erro": ...}

    Sucesso:
      GET /pedidos        -> 200 {"pedidos": [lista ordenada por id]}
      GET /pedidos/<id>   -> 200 pedido
      POST /pedidos       -> 201 pedido criado       (grava)
      PUT /pedidos/<id>   -> 200 pedido novo         (substitui)
      DELETE /pedidos/<id>-> 204 None                (remove)
    Guarde e devolva CÓPIAS (dict(...)) — quem chama não pode alterar o estado por fora.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
