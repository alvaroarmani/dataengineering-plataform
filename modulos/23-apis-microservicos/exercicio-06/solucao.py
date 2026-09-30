"""Exercício 06 (M23) — Evolução de contrato: o que quebra os consumidores.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""


def mudancas(antigo: dict, novo: dict) -> dict:
    """antigo/novo = {"requisicao": {campo: {"tipo", "obrigatorio"}}, "resposta": {campo: {"tipo"}}}.
    Classifique em {"incompativeis": [...], "compativeis": [...]} (listas ordenadas), com itens no
    formato "lado.campo:motivo":
      resposta: campo removido -> incompatível "removido"; tipo mudou -> incompatível "tipo";
                campo novo -> compatível "adicionado"
      requisição: campo novo obrigatório -> incompatível "novo_obrigatorio";
                  campo novo opcional -> compatível "adicionado";
                  campo existente passou a obrigatório -> incompatível "virou_obrigatorio";
                  obrigatório passou a opcional -> compatível "virou_opcional";
                  tipo mudou -> incompatível "tipo"; campo removido -> compatível "removido"
                  (o servidor passa a ignorá-lo)"""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def proxima_versao(versao: str, m: dict) -> str:
    """Semver "MAJOR.MINOR.PATCH": incompatível -> MAJOR+1.0.0; só compatíveis -> MAJOR.MINOR+1.0;
    nada -> MAJOR.MINOR.PATCH+1. Versão malformada -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
