"""Exercício 01 (M10) — Cache de camadas: o que reconstrói quando um arquivo muda.

Rode `pytest -q`. Detalhes no enunciado (exercicio-01.md).
"""


def passos_reconstruidos(dockerfile: list, alterados: dict) -> list:
    """dockerfile = [{"instr": texto, "copia": [arquivos ou pastas terminadas em "/" ou "."], "seg": duração}].
    alterados = {"arquivos": [caminhos modificados], "instrucoes": [índices cujo texto mudou]}.
    O primeiro passo "sujo" é o de menor índice que teve o texto alterado OU copia algum arquivo alterado
    ("." copia tudo). Retorne os índices desse passo até o fim; nada sujo -> []."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def tempo_de_build(dockerfile: list, alterados: dict) -> int:
    """Soma dos segundos dos passos reconstruídos (os do cache custam 0)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
