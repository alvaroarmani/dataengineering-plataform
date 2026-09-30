"""Exercício 09 (M12) — Qualidade de dados em corridas REAIS de táxi de NY (mini-caso).

Dados: datasets/amostras/nyc_taxi_2024_01_amostra.csv — 2.617 corridas reais de jan/2024 (TLC de
Nova York), com as anomalias que existem de verdade no arquivo oficial. Rode `pytest -q`.

Regras de qualidade, EM ORDEM DE PRIORIDADE (a primeira que uma linha violar é o motivo dela):
  1. fora_do_periodo             — embarque fora de jan/2024 (pickup < 2024-01-01 ou >= 2024-02-01)
  2. desembarque_antes_embarque  — tpep_dropoff_datetime < tpep_pickup_datetime
  3. tarifa_negativa             — fare_amount < 0
  4. passageiros_invalidos       — passenger_count nulo OU <= 0
  5. distancia_absurda           — trip_distance > 100 (milhas)
"""
import pandas as pd


def perfilar(df: pd.DataFrame) -> dict:
    """Retorne {regra: nº de linhas que violam a regra} para as 5 regras (uma linha pode violar
    várias — aqui cada regra conta de forma independente). Valores como int."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def separar_quarentena(df: pd.DataFrame) -> tuple:
    """Separe o lote em (validas, quarentena).

    - validas: linhas que não violam NENHUMA regra.
    - quarentena: linhas que violam ao menos uma, com uma coluna nova 'motivo' = a regra de MAIOR
      prioridade violada (ver ordem no topo do arquivo).
    Preserve a ordem original das linhas e reinicie o índice (reset_index(drop=True)) nas duas saídas.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def aprovar_lote(df: pd.DataFrame, max_invalidos_pct: float) -> bool:
    """Portão de qualidade: True se o % de linhas em quarentena for <= max_invalidos_pct.
    Lote vazio é aprovado (não há nada inválido)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
