"""Exercício 02 (M10) — .dockerignore com curingas e negação.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""

from fnmatch import fnmatch


def no_contexto(arquivos: list, regras: list) -> list:
    """Para cada caminho, percorra as regras em ordem; a ÚLTIMA que casar decide:
      regra normal -> ignora; regra "!..." -> reinclui. Nenhuma casa -> incluído.
    Casamento: "pasta/" = prefixo; "**/padrão" = o padrão casa com algum trecho final do caminho ou com
    algum nome dentro dele; senão, fnmatch no caminho inteiro (ou a regra é uma pasta pai do caminho).
    Linhas vazias ou começando com "#" são ignoradas. Retorne os incluídos, ordenados."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def tamanho_do_contexto(tamanhos: dict, regras: list) -> int:
    """tamanhos = {caminho: bytes}. Soma dos bytes dos caminhos que vão para o contexto."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
