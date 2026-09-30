"""Exercício 05 (M13) — Plano do Terraform: atualizar, substituir e proteger.

Rode `pytest -q`. Detalhes no enunciado (exercicio-05.md).
"""


def plano(atual: dict, desejado: dict, imutaveis: dict) -> dict:
    """atual/desejado = {nome: {"tipo": ..., atributos...}}; imutaveis = {tipo: [atributos que forçam
    substituição]}. O atributo "prevent_destroy" (em `atual`) não é comparado — é uma proteção.

    Retorne {"criar": [...], "atualizar": {nome: [atributos alterados]}, "substituir": [...],
             "destruir": [...]} (listas e atributos ordenados):
      - só no desejado -> criar;  só no atual -> destruir
      - nos dois com atributos diferentes (considerando atributos que existem em só um dos lados):
          algum alterado é imutável para o tipo (ou o "tipo" mudou) -> substituir;  senão -> atualizar
    Se um recurso com prevent_destroy=True seria destruído ou substituído -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
