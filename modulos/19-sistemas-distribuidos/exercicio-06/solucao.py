"""Exercício 06 (M19) — Conflitos: last-write-wins x vetores de versão.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""


def lww(versoes: list) -> dict:
    """versoes = [{"valor", "ts", "no"}]. Fica a de MAIOR ts; empate: maior nome de nó.
    Lista vazia -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def comparar_vetores(a: dict, b: dict) -> str:
    """Vetores {no: contador} (nó ausente = 0). Retorne:
      "igual"       todos os contadores iguais
      "antes"       a <= b em todos os nós e diferente em algum (b sucede a)
      "depois"      o contrário
      "concorrente" cada um é maior em algum nó"""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def versoes_sobreviventes(versoes: list) -> list:
    """versoes = [{"valor", "vetor"}]. Descarte toda versão que vem "antes" de alguma outra (ou é
    "igual" a uma que já ficou). Retorne os valores sobreviventes, ordenados — mais de um = conflito."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
