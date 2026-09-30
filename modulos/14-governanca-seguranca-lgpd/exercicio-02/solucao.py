"""Exercício 02 (M14) — Auditoria do catálogo de dados.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""

from datetime import date


def auditar_catalogo(catalogo: dict, hoje: str, dias_abandono: int = 90) -> dict:
    """catalogo = {ativo: {"dono", "descricao", "ultimo_acesso" ('AAAA-MM-DD' ou None), "pii": bool}}.
    Problemas por ativo:
      "sem_dono"       dono None ou só espaços
      "sem_descricao"  descrição None ou só espaços
      "abandonado"     nunca acessado (None) ou último acesso há MAIS de `dias_abandono` dias
    Crítico: ativo com pii=True e sem dono.
    Retorne {"problemas": {ativo: [problemas ordenados]} (só ativos com problema, em ordem de nome),
             "criticos": [ordenados]}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
