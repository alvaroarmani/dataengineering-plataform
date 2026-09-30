"""Exercício 04 (M14) — RBAC com herança, curinga e negação explícita.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def pode_acessar(usuario: str, recurso: str, acao: str, politicas: dict) -> bool:
    """politicas = {"usuarios": {usuario: [papeis]},
                    "papeis": {papel: {"herda": [papeis], "permite": [(padrao, acao)], "nega": [(padrao, acao)]}}}
    - padrao "schema.*" casa com qualquer recurso "schema.<algo>"; senão, só o nome exato.
    - acao "*" numa regra vale para qualquer ação.
    - Papéis efetivos = os do usuário + todos os herdados (transitivamente; ciclos não podem travar).
    - Alguma regra "nega" que case -> False. Senão, alguma "permite" que case -> True. Senão -> False.
    Usuário desconhecido -> False."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
