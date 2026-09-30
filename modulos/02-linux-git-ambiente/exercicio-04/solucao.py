"""Exercício 04 (M2) — Lendo o git status --porcelain.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def resumo_status(saida: str) -> dict:
    """saida = texto do `git status --porcelain` (v1). Cada linha: XY<espaço>caminho, com X e Y em
    " MADRCU?" (outra letra, ou sem o espaço na 3ª posição -> linha malformada).
      X (índice) != " " e != "?"  -> arquivo está em "staged"
      Y (árvore) != " " e != "?"  -> arquivo está em "nao_staged" (pode estar nas duas listas)
      "??"                        -> "untracked"
      X == "R"                    -> caminho é "antigo -> novo": entra em "renomeados" como (antigo, novo)
                                     e em "staged" pelo nome NOVO
    Retorne as quatro listas ordenadas. Linha em branco é ignorada; linha malformada -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
