"""Testes do Exercício 11 (M05) — star schema com dados REAIS. Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import dim_zona, fato_corridas, receita_por_borough  # noqa: E402

AMOSTRAS = RAIZ / "datasets" / "amostras"


@pytest.fixture(scope="module")
def zonas():
    return pd.read_csv(AMOSTRAS / "taxi_zone_lookup.csv")


@pytest.fixture(scope="module")
def corridas():
    return pd.read_csv(AMOSTRAS / "nyc_taxi_2024_01_amostra.csv",
                       parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"])


@pytest.fixture(scope="module")
def dim(zonas):
    return dim_zona(zonas)


@pytest.fixture(scope="module")
def fato(corridas, dim):
    return fato_corridas(corridas, dim)


# ---------- dim_zona ----------
def test_dim_zona_estrutura(dim):
    assert list(dim.columns) == ["zona_sk", "location_id", "borough", "zona"]
    assert len(dim) == 265
    assert list(dim["zona_sk"]) == list(range(1, 266))
    assert dim.iloc[0].to_dict() == {"zona_sk": 1, "location_id": 1, "borough": "EWR", "zona": "Newark Airport"}


def test_dim_zona_sem_atributo_nulo(dim):
    assert dim["borough"].notna().all() and dim["zona"].notna().all()
    # na tabela oficial, a zona 265 ("Outside of NYC") tem borough "N/A" — que o pandas lê como nulo
    assert dim.iloc[-1].to_dict() == {"zona_sk": 265, "location_id": 265,
                                     "borough": "Desconhecido", "zona": "Outside of NYC"}


# ---------- fato_corridas ----------
def test_fato_colunas_e_grao(fato):
    assert list(fato.columns) == ["viagem_id", "data_sk", "zona_embarque_sk", "zona_desembarque_sk",
                                  "passageiros", "distancia", "valor_total", "gorjeta", "duracao_min"]
    assert len(fato) == 2527
    assert fato["viagem_id"].is_unique and fato["viagem_id"].is_monotonic_increasing


def test_fato_primeira_linha(fato):
    linha = fato.iloc[0].to_dict()
    assert linha["viagem_id"] == 34 and linha["data_sk"] == 20240101
    assert linha["zona_embarque_sk"] == 74 and linha["zona_desembarque_sk"] == 164
    assert linha["valor_total"] == 47.41 and linha["duracao_min"] == 26.42


def test_fato_integridade_referencial(fato, dim):
    sks = set(dim["zona_sk"])
    assert fato["zona_embarque_sk"].notna().all() and fato["zona_desembarque_sk"].notna().all()
    assert set(fato["zona_embarque_sk"]) <= sks and set(fato["zona_desembarque_sk"]) <= sks


def test_fato_so_tem_corridas_validas_de_janeiro(fato):
    assert fato["data_sk"].between(20240101, 20240131).all()
    assert (fato["valor_total"] > 0).all() and (fato["duracao_min"] >= 0).all()


# ---------- receita_por_borough (role-playing) ----------
def test_receita_por_borough_de_embarque(fato, dim):
    assert receita_por_borough(fato, dim, "embarque").to_dict("records") == [
        {"borough": "Manhattan", "corridas": 2237, "receita": 50145.85},
        {"borough": "Queens", "corridas": 246, "receita": 19362.34},
        {"borough": "Bronx", "corridas": 5, "receita": 2192.12},
        {"borough": "Brooklyn", "corridas": 29, "receita": 972.3},
        {"borough": "Unknown", "corridas": 10, "receita": 418.67},
    ]


def test_mesma_dimensao_outro_papel_da_outro_resultado(fato, dim):
    des = receita_por_borough(fato, dim, "desembarque")
    assert des.iloc[:3].to_dict("records") == [
        {"borough": "Manhattan", "corridas": 2277, "receita": 55105.27},
        {"borough": "Desconhecido", "corridas": 18, "receita": 6000.29},   # corridas que saem de NY
        {"borough": "Queens", "corridas": 108, "receita": 5535.15},
    ]


def test_reconciliacao_nenhuma_corrida_some(fato, dim):
    total = fato["valor_total"].sum()
    for papel in ("embarque", "desembarque"):
        agg = receita_por_borough(fato, dim, papel)
        assert agg["corridas"].sum() == len(fato)
        assert agg["receita"].sum() == pytest.approx(total, abs=0.05)


def test_subconjunto_de_um_fornecedor(corridas, dim):
    f1 = fato_corridas(corridas[corridas["VendorID"] == 1], dim)
    assert len(f1) == 698
    assert receita_por_borough(f1, dim, "embarque").to_dict("records") == [
        {"borough": "Manhattan", "corridas": 613, "receita": 13080.99},
        {"borough": "Queens", "corridas": 65, "receita": 4975.72},
        {"borough": "Brooklyn", "corridas": 14, "receita": 406.22},
        {"borough": "Unknown", "corridas": 4, "receita": 113.6},
        {"borough": "Bronx", "corridas": 2, "receita": 35.86},
    ]


def test_papel_invalido(fato, dim):
    with pytest.raises(ValueError):
        receita_por_borough(fato, dim, "origem")
