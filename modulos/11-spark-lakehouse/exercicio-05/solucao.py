"""Exercício 05 (M11) — Broadcast ou sort-merge? A escolha do join.

Rode `pytest -q`. Detalhes no enunciado (exercicio-05.md).
"""


BROADCASTAVEL = {"inner": {"esquerda", "direita"}, "left": {"direita"}, "right": {"esquerda"},
                 "left_semi": {"direita"}, "left_anti": {"direita"}, "full": set()}


def estrategia_join(esquerda_mb: float, direita_mb: float, tipo: str = "inner", limite_mb: float = 10) -> dict:
    """Retorne {"estrategia": "broadcast_hash" | "sort_merge", "broadcast": "esquerda"|"direita"|None,
    "lados_com_shuffle": 0 ou 2}. Regras:
      - candidatos = lados permitidos para o tipo (BROADCASTAVEL) com tamanho <= limite_mb;
      - havendo candidatos, faça broadcast do MENOR (empate: direita) -> 0 lados com shuffle;
      - senão, sort-merge -> 2 lados com shuffle.
    limite_mb <= 0 desliga o broadcast automático. Tipo desconhecido -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
