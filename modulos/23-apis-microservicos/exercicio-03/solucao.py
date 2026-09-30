"""Exercício 03 (M23) — Idempotency-Key do lado do servidor.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""

import json


def tratar(armazem: dict, chave: str, corpo: dict, agora: int, ttl_seg: int = 86_400) -> tuple:
    """armazem = {"chaves": {chave: {"corpo", "resposta", "criado_em"}}, "proximo_id": int, "cobrancas": [ ]}
    (é alterado no lugar — é o "banco" do servidor).
      - chave vista há menos de ttl_seg segundos e corpo IGUAL -> devolve a resposta guardada: (200, resposta, True)
      - chave vista (válida) com corpo DIFERENTE -> (422, {"erro": ...}, False), nada é executado
      - chave nova ou expirada -> executa: cria a cobrança {"id": proximo_id, **corpo}, incrementa
        proximo_id, guarda a resposta e devolve (201, resposta, False)
    Chave vazia -> ValueError. O terceiro valor indica se foi um replay."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
