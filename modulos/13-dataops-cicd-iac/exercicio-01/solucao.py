"""Exercício 01 (M13) — Proteção de branch: o PR pode entrar?.

Rode `pytest -q`. Detalhes no enunciado (exercicio-01.md).
"""


def avaliar_pr(pr: dict, regras: dict) -> dict:
    """pr = {"autor", "checks": [(nome, status)] em ordem cronológica, "aprovacoes": [usuarios],
             "arquivos": [caminhos], "atualizado": bool}
    regras = {"checks_obrigatorios": [nomes], "aprovacoes_min": int, "codeowners": {prefixo: dono}}

    Bloqueios (formato "tipo:detalhe"), todos os que se aplicarem, em ordem alfabética:
      "check:<nome>"          check obrigatório ausente ou cujo ÚLTIMO status não é "pass"
      "aprovacoes:<n>/<min>"  aprovações válidas abaixo do mínimo (aprovação do autor não conta;
                              o mesmo revisor conta uma vez)
      "codeowner:<dono>"      algum arquivo começa com um prefixo do CODEOWNERS e o dono não aprovou
                              (se o autor é o dono, ainda precisa de OUTRO aprovador — já coberto acima)
      "desatualizado"         branch não está atualizado com a main
    Retorne {"pode": sem bloqueios, "bloqueios": [...]}.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
