import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import blocos_lidos, fracao_podada  # noqa: E402

# 6 row groups de vendas, gravados ordenados por data
BLOCOS = [
    {"data": ("2026-01-01", "2026-01-31"), "valor": (5, 900)},
    {"data": ("2026-02-01", "2026-02-28"), "valor": (8, 4_000)},
    {"data": ("2026-03-01", "2026-03-31"), "valor": (3, 700)},
    {"data": ("2026-04-01", "2026-04-30"), "valor": (10, 12_000)},
    {"data": ("2026-05-01", "2026-05-31"), "valor": None},            # sem estatística de valor
    {"data": ("2026-06-01", "2026-06-30"), "valor": (1, 50)},
]


def test_filtro_por_data():
    assert blocos_lidos(BLOCOS, {"data": ("2026-02-15", "2026-04-10")}) == [1, 2, 3]
    assert fracao_podada(BLOCOS, {"data": ("2026-02-15", "2026-04-10")}) == 0.5


def test_dois_filtros_precisam_passar():
    f = {"data": ("2026-01-01", "2026-06-30"), "valor": (1_000, None)}
    assert blocos_lidos(BLOCOS, f) == [1, 3, 4]              # o bloco 4 não tem estatística de valor


def test_fronteiras_inclusivas_e_sem_limite():
    assert blocos_lidos(BLOCOS, {"data": ("2026-03-31", "2026-04-01")}) == [2, 3]
    assert blocos_lidos(BLOCOS, {"data": (None, "2026-01-15")}) == [0]


def test_dados_desordenados_nao_podam():
    desordenados = [{"data": ("2026-01-02", "2026-06-29")}] * 6
    assert fracao_podada(desordenados, {"data": ("2026-03-01", "2026-03-02")}) == 0.0


def test_faixa_invalida_e_vazio():
    with pytest.raises(ValueError):
        blocos_lidos(BLOCOS, {"valor": (10, 1)})
    assert fracao_podada([], {"valor": (1, 2)}) == 0.0
