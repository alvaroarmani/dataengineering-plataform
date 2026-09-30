"""Testes do Exercício 09 (M12) — qualidade em dados REAIS. Faça todos passarem: pytest -q

Os valores esperados foram medidos na amostra real (datasets/amostras). Há testes num SUBCONJUNTO
(só VendorID=2) e em casos construídos — então decorar números não passa: é preciso implementar a regra.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import aprovar_lote, perfilar, separar_quarentena  # noqa: E402

AMOSTRA = RAIZ / "datasets" / "amostras" / "nyc_taxi_2024_01_amostra.csv"
REGRAS = ["fora_do_periodo", "desembarque_antes_embarque", "tarifa_negativa",
          "passageiros_invalidos", "distancia_absurda"]


@pytest.fixture(scope="module")
def corridas():
    return pd.read_csv(AMOSTRA, parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"])


def _linha(**kw):
    base = dict(viagem_id=1, VendorID=1, tpep_pickup_datetime=pd.Timestamp("2024-01-10 10:00"),
                tpep_dropoff_datetime=pd.Timestamp("2024-01-10 10:20"), passenger_count=1.0,
                trip_distance=3.0, PULocationID=161, DOLocationID=236, payment_type=1,
                fare_amount=15.0, tip_amount=3.0, total_amount=22.0)
    base.update(kw)
    return base


# ---------- perfilar ----------
def test_perfil_da_amostra_real(corridas):
    assert perfilar(corridas) == {
        "fora_do_periodo": 18, "desembarque_antes_embarque": 20, "tarifa_negativa": 56,
        "passageiros_invalidos": 211, "distancia_absurda": 20,
    }


def test_perfil_de_um_fornecedor(corridas):
    # a sujeira real não é uniforme: o fornecedor 2 concentra tarifa negativa e fora do período
    assert perfilar(corridas[corridas["VendorID"] == 2]) == {
        "fora_do_periodo": 18, "desembarque_antes_embarque": 0, "tarifa_negativa": 56,
        "passageiros_invalidos": 92, "distancia_absurda": 17,
    }


def test_perfil_conta_nulo_e_zero_como_passageiro_invalido():
    df = pd.DataFrame([_linha(passenger_count=None), _linha(passenger_count=0.0), _linha()])
    assert perfilar(df)["passageiros_invalidos"] == 2


# ---------- separar_quarentena ----------
def test_quarentena_particiona_o_lote(corridas):
    validas, quarentena = separar_quarentena(corridas)
    assert len(validas) == 2321 and len(quarentena) == 296
    assert set(validas["viagem_id"]).isdisjoint(set(quarentena["viagem_id"]))
    assert len(validas) + len(quarentena) == len(corridas)
    assert list(quarentena.columns) == list(corridas.columns) + ["motivo"]


def test_validas_nao_violam_nenhuma_regra(corridas):
    validas, _ = separar_quarentena(corridas)
    assert all(v == 0 for v in perfilar(validas).values())


def test_motivos_respeitam_a_prioridade(corridas):
    _, quarentena = separar_quarentena(corridas)
    assert quarentena["motivo"].value_counts().to_dict() == {
        "passageiros_invalidos": 192, "tarifa_negativa": 55, "desembarque_antes_embarque": 20,
        "fora_do_periodo": 18, "distancia_absurda": 11,
    }


def test_prioridade_em_linha_que_viola_varias_regras():
    df = pd.DataFrame([
        _linha(viagem_id=1, fare_amount=-5.0, passenger_count=0.0, trip_distance=500.0),  # 3 regras
        _linha(viagem_id=2, tpep_pickup_datetime=pd.Timestamp("2023-12-31 23:50"),
               tpep_dropoff_datetime=pd.Timestamp("2023-12-31 23:40")),                    # 2 regras
        _linha(viagem_id=3),                                                                # válida
    ])
    validas, quarentena = separar_quarentena(df)
    assert list(validas["viagem_id"]) == [3]
    assert list(quarentena["motivo"]) == ["tarifa_negativa", "fora_do_periodo"]


def test_quarentena_preserva_ordem_e_reinicia_indice(corridas):
    validas, quarentena = separar_quarentena(corridas)
    assert list(validas.index) == list(range(len(validas)))
    assert quarentena["viagem_id"].is_monotonic_increasing


# ---------- aprovar_lote ----------
def test_portao_de_qualidade(corridas):
    # 296/2617 = 11,31% em quarentena
    assert aprovar_lote(corridas, 12.0) is True
    assert aprovar_lote(corridas, 11.0) is False


def test_portao_lote_vazio_e_limite_exato():
    assert aprovar_lote(pd.DataFrame([_linha()]).iloc[0:0], 0.0) is True
    df = pd.DataFrame([_linha(viagem_id=1), _linha(viagem_id=2, fare_amount=-1.0)])  # 50% inválido
    assert aprovar_lote(df, 50.0) is True
    assert aprovar_lote(df, 49.9) is False
