"""Exercício 03 (M18) — Cache key-value com TTL e despejo LRU.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""

from collections import OrderedDict


class Cache:
    """Cache em memória com TTL (em segundos) e despejo LRU. O tempo é passado explicitamente
    (`agora`, em segundos) para os testes serem determinísticos."""

    def __init__(self, capacidade: int):
        """capacidade < 1 -> ValueError. Guarde os contadores: hits, misses, despejos, expiradas."""
        # SEU CÓDIGO AQUI
        raise NotImplementedError

    def set(self, chave, valor, agora: float, ttl: float = None) -> None:
        """Grava (ou sobrescreve) a chave; ela passa a ser a MAIS recentemente usada.
        Se for uma chave NOVA e o cache estiver cheio: primeiro remova todas as chaves vencidas
        (conte em `expiradas`); se ainda estiver cheio, despeje a MENOS recentemente usada (`despejos`)."""
        # SEU CÓDIGO AQUI
        raise NotImplementedError

    def get(self, chave, agora: float):
        """Valor da chave (hit; ela vira a mais recente) ou None (miss).
        Chave vencida (agora >= gravada + ttl) é removida na leitura, conta em `expiradas` e é miss."""
        # SEU CÓDIGO AQUI
        raise NotImplementedError

    def hit_rate(self) -> float:
        """hits / (hits + misses), 2 casas; 0.0 sem leituras."""
        # SEU CÓDIGO AQUI
        raise NotImplementedError
