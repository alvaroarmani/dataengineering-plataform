"""Exercício 02 (M12) — Validar um data contract.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""


TIPOS = {"int": (int,), "float": (int, float), "str": (str,), "bool": (bool,)}


def validar(registro: dict, contrato: dict) -> list:
    """contrato = {campo: {"tipo": "int"|"float"|"str"|"bool", "obrigatorio": bool, "nulo": bool}}.

    Retorne a lista ORDENADA de violações no formato "campo:motivo":
      - "campo:ausente"      campo obrigatório que não está no registro
      - "campo:nulo"         valor None num campo com "nulo": False
      - "campo:tipo"         tipo errado. "float" aceita int (JSON não distingue 1 de 1.0);
                             bool NUNCA vale como int nem como float
      - "campo:nao_previsto" campo do registro que não existe no contrato
    Campo opcional ausente não é violação. Tipo desconhecido no contrato -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def validar_lote(registros: list, contrato: dict) -> dict:
    """{"validos": qtd, "invalidos": qtd, "violacoes": {violacao: ocorrencias}}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
