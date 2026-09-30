"""Exercício 02 (M23) — Paginação por offset x por cursor com dados mudando.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""


def pagina_offset(itens: list, pagina: int, tamanho: int) -> list:
    """Página `pagina` (começa em 1) de `itens`. pagina < 1 ou tamanho < 1 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def pagina_cursor(itens: list, depois_de, tamanho: int) -> tuple:
    """itens = dicts com "id" (a API os devolve ordenados por id, mas a lista pode vir desordenada).
    Retorne (pagina, proximo_cursor): os `tamanho` primeiros com id > depois_de (None = do começo),
    em ordem de id; proximo_cursor = id do último da página, ou None se NÃO houver mais itens depois dele."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def ingerir_com_cursor(buscar, tamanho: int) -> list:
    """buscar(depois_de, tamanho) -> (pagina, proximo_cursor), como a API. Percorra todas as páginas
    e devolva os ids na ordem lida. Proteção: se o cursor não avançar (API com bug), ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
