"""Exercício 11 (M05) — Star schema com dados REAIS de táxi de NY (mini-caso).

Dados reais (datasets/amostras/):
  - nyc_taxi_2024_01_amostra.csv — 2.617 corridas de jan/2024 (TLC de Nova York)
  - taxi_zone_lookup.csv         — tabela oficial de 265 zonas (LocationID, Borough, Zone, service_zone)
Rode `pytest -q`.

Modelo-alvo:
  dim_zona(zona_sk, location_id, borough, zona)
  fato_corridas(viagem_id, data_sk, zona_embarque_sk, zona_desembarque_sk,
                passageiros, distancia, valor_total, gorjeta, duracao_min)
A dim_zona é ROLE-PLAYING: a mesma dimensão serve ao embarque e ao desembarque.
"""
import pandas as pd


def dim_zona(zonas: pd.DataFrame) -> pd.DataFrame:
    """Dimensão de zona com chave substituta.

    - Ordene por LocationID; zona_sk = 1, 2, 3, ...
    - Colunas: zona_sk, location_id (int), borough, zona.
    - Uma dimensão NÃO pode ter atributo nulo: substitua nulos de borough/zona por "Desconhecido".
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def fato_corridas(corridas: pd.DataFrame, dim: pd.DataFrame) -> pd.DataFrame:
    """Fato no grão de 1 linha por corrida VÁLIDA, com as colunas do modelo-alvo, ordenada por viagem_id
    (índice reiniciado).

    - Válida: total_amount > 0, embarque dentro de jan/2024 e desembarque >= embarque.
    - data_sk = data do embarque como int AAAAMMDD (ex.: 20240115).
    - zona_embarque_sk / zona_desembarque_sk = zona_sk da dim para PULocationID / DOLocationID.
    - passageiros=passenger_count, distancia=trip_distance, valor_total=total_amount,
      gorjeta=tip_amount, duracao_min = (desembarque - embarque) em minutos, arredondada a 2 casas.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def receita_por_borough(fato: pd.DataFrame, dim: pd.DataFrame, papel: str) -> pd.DataFrame:
    """Receita por borough no PAPEL pedido ('embarque' ou 'desembarque'; outro valor → ValueError).

    Colunas: borough, corridas (nº de linhas da fato), receita (soma de valor_total, 2 casas).
    Ordene por receita desc (desempate por borough). A soma das receitas TEM de bater com o total
    da fato — nenhuma corrida pode sumir na agregação.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
