"""Testes do Exercício 05 (M15). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import armazenamento_tb, proposta, vazao  # noqa: E402


def test_vazao():
    assert vazao(50_000_000) == {"media_s": 578.7, "pico_s": 1736.1}   # 50 mi/dia ≈ 580/s
    assert vazao(86_400, 1) == {"media_s": 1.0, "pico_s": 1.0}
    assert vazao(10_000_000, 5) == {"media_s": 115.7, "pico_s": 578.7}


def test_armazenamento():
    assert armazenamento_tb(50_000_000, 1_000, 365) == 18.25
    assert armazenamento_tb(50_000_000, 1_000, 365, replicas=3, compressao=5) == 10.95   # Parquet comprime
    assert armazenamento_tb(2_000_000_000, 400, 30, 3, 4) == 18.0


def test_proposta_relatorio_diario():
    assert proposta({"eventos_dia": 2_000_000, "bytes_evento": 800, "latencia_seg": 86_400,
                     "retencao_dias": 730}) == {
        "processamento": "batch", "motor": "sql-warehouse", "pico_s": 69.4, "armazenamento_tb": 1.168}


def test_proposta_telemetria_em_tempo_real():
    assert proposta({"eventos_dia": 2_000_000_000, "bytes_evento": 400, "latencia_seg": 5,
                     "retencao_dias": 30, "replicas": 3, "compressao": 4, "fator_pico": 4}) == {
        "processamento": "streaming", "motor": "spark", "pico_s": 92592.6, "armazenamento_tb": 18.0}


def test_proposta_painel_de_15_minutos():
    r = proposta({"eventos_dia": 300_000_000, "bytes_evento": 1_500, "latencia_seg": 900, "retencao_dias": 90})
    assert r["processamento"] == "micro-batch"
    assert r["motor"] == "sql-warehouse"          # 450 GB/dia: um warehouse dá conta, sem cluster
    assert r["armazenamento_tb"] == 40.5


@pytest.mark.parametrize("latencia, esperado", [(3600, "batch"), (3599, "micro-batch"),
                                                (60, "micro-batch"), (59.9, "streaming")])
def test_fronteiras_de_latencia(latencia, esperado):
    req = {"eventos_dia": 1_000, "bytes_evento": 100, "latencia_seg": latencia, "retencao_dias": 1}
    assert proposta(req)["processamento"] == esperado


def test_fronteira_de_volume():
    base = {"bytes_evento": 1_000, "latencia_seg": 86_400, "retencao_dias": 1}
    assert proposta({**base, "eventos_dia": 500_000_000})["motor"] == "sql-warehouse"   # exatamente 500 GB
    assert proposta({**base, "eventos_dia": 500_000_001})["motor"] == "spark"


@pytest.mark.parametrize("chamada", [
    lambda: vazao(-1),
    lambda: vazao(100, 0.5),
    lambda: armazenamento_tb(1, 1, 1, replicas=0),
    lambda: armazenamento_tb(1, 1, 1, compressao=0),
    lambda: proposta({"eventos_dia": 10, "bytes_evento": 10, "retencao_dias": 1}),   # sem latência
])
def test_entradas_invalidas(chamada):
    with pytest.raises(ValueError):
        chamada()
