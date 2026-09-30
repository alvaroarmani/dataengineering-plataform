"""Testes do Exercício 05 (M18). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import aplicar_retencao, reagregar, rollup  # noqa: E402

# Temperatura de um sensor (°C). No 1º minuto ele reporta muito (a cada 10 s); depois, só 1 vez.
PONTOS = [(0, 20.0), (10, 20.0), (20, 20.0), (30, 20.0), (40, 20.0), (50, 20.0),
          (60, 26.0),
          (130, 22.0), (170, 24.0),
          (3600, 30.0), (3650, 31.0)]


def test_rollup_por_minuto():
    assert rollup(PONTOS, 60) == {
        0: {"n": 6, "min": 20.0, "max": 20.0, "media": 20.0},
        60: {"n": 1, "min": 26.0, "max": 26.0, "media": 26.0},
        120: {"n": 2, "min": 22.0, "max": 24.0, "media": 23.0},
        3600: {"n": 2, "min": 30.0, "max": 31.0, "media": 30.5},
    }


def test_rollup_ordena_e_ignora_ordem_de_chegada():
    embaralhado = list(reversed(PONTOS))
    r = rollup(embaralhado, 60)
    assert list(r) == [0, 60, 120, 3600]
    assert r == rollup(PONTOS, 60)


def test_reagregar_nao_e_media_de_medias():
    por_minuto = rollup(PONTOS, 60)
    por_hora = reagregar(por_minuto, 3600)
    # média de médias daria (20 + 26 + 23) / 3 = 23.0 — ERRADO: o 1º minuto tem 6 pontos
    assert por_hora[0] == {"n": 9, "min": 20.0, "max": 26.0, "media": 21.33}
    assert por_hora[3600] == {"n": 2, "min": 30.0, "max": 31.0, "media": 30.5}


def test_reagregar_bate_com_o_rollup_direto():
    assert reagregar(rollup(PONTOS, 60), 3600) == rollup(PONTOS, 3600)
    assert reagregar(rollup(PONTOS, 10), 60) == rollup(PONTOS, 60)


def test_retencao():
    recentes, antigos = aplicar_retencao(PONTOS, agora=3700, janela_bruta_seg=600, bucket_seg=60)
    assert recentes == [(3600, 30.0), (3650, 31.0)]
    assert antigos == rollup(PONTOS[:-2], 60)
    assert sum(r["n"] for r in antigos.values()) + len(recentes) == len(PONTOS)   # nada some sem rastro


def test_retencao_fronteira_inclusiva():
    recentes, antigos = aplicar_retencao(PONTOS, agora=3700, janela_bruta_seg=100, bucket_seg=60)
    assert recentes == [(3600, 30.0), (3650, 31.0)]          # ts == agora - janela fica bruto
    assert 3600 not in antigos


def test_vazio_e_bucket_invalido():
    assert rollup([], 60) == {}
    assert reagregar({}, 3600) == {}
    with pytest.raises(ValueError):
        rollup(PONTOS, 0)
    with pytest.raises(ValueError):
        reagregar(rollup(PONTOS, 60), -1)
