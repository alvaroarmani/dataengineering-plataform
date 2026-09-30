"""Exercício 03 (M20) — Rolling update: maxSurge e maxUnavailable.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""


def rolling_update(replicas: int, max_surge: int, max_unavailable: int) -> list:
    """Simule a troca. Estado: antigos (prontos), novos_prontos, novos_pendentes. A cada passo:
      1. remova antigos: pode remover até (antigos + novos_prontos) - (replicas - max_unavailable),
         sem ficar negativo;
      2. crie novos: até o total (antigos + novos_prontos + novos_pendentes) chegar a replicas + max_surge,
         sem passar de `replicas` novos no total;
      3. fim do passo: os pendentes ficam prontos. Registre (antigos, novos_prontos).
    Repita até (0, replicas). max_surge e max_unavailable ambos 0 -> ValueError (a troca nunca anda)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def resumo(passos: list, replicas: int) -> dict:
    """{"passos": len(passos), "min_disponivel": menor (antigos + novos) ao longo dos passos E do estado
    inicial (replicas), "max_total": maior (antigos + novos)}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
