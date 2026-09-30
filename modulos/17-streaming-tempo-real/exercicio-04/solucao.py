"""Exercício 04 (M17) — Consumer group: atribuição de partições e lag por consumidor.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def atribuir_range(n_particoes: int, consumidores: list) -> dict:
    """Ordene os consumidores; cada um recebe n // c partições CONTÍGUAS, e os n % c primeiros recebem
    uma a mais. Retorne {consumidor: [particoes]} para todos (ociosos com lista vazia).
    Sem consumidores -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def lag_por_consumidor(fim: dict, commits: dict, atribuicao: dict) -> dict:
    """fim = {particao: offset final}; commits = {particao: offset commitado} (ausente = 0).
    Retorne {consumidor: soma do lag das suas partições} e, na chave "_mais_atrasado", o consumidor
    de maior lag (empate: ordem alfabética; None se todos com lag 0).
    Commit maior que o offset final -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
