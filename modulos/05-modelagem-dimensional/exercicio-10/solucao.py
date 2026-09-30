"""Exercício 10 (M5) — Bridge table: ratear sem contar em dobro.

Rode `pytest -q`. Detalhes no enunciado (exercicio-10.md).
"""


def alocar_por_ponte(fatos: list, ponte: dict) -> dict:
    """fatos = [(pedido_id, produto_id, receita)]; ponte = {produto_id: {categoria: peso}}.
    - Os pesos de cada produto precisam somar 1 (tolerância 1e-6) -> senão ValueError.
    - Receita de produto fora da ponte vai para a categoria "sem_categoria".
    Retorne {categoria: receita alocada com 2 casas}, com as categorias em ordem alfabética.
    A soma do resultado deve bater com a receita total (reconciliação)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def soma_ingenua(fatos: list, ponte: dict) -> float:
    """O ERRO clássico: soma das receitas por categoria contando a receita inteira em cada categoria
    do produto (sem pesos). Retorne o total "por categoria" com 2 casas (para comparar com o real)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
