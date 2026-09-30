import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import apurar_eleicao, log_ok  # noqa: E402


@pytest.mark.parametrize("cand, eleitor, ok", [
    ((3, 10), (2, 50), True),      # termo mais novo vence, mesmo com log mais curto
    ((2, 50), (3, 10), False),
    ((3, 10), (3, 10), True),      # igual: pode votar
    ((3, 9), (3, 10), False),      # mesmo termo, mais curto
])
def test_log_ok(cand, eleitor, ok):
    assert log_ok(cand, eleitor) is ok


def test_candidato_desatualizado_nao_vence():
    eleitores = {"a": (3, 10), "b": (3, 12), "c": (3, 12), "d": (2, 40), "e": (3, 11)}
    r = apurar_eleicao([("a", (3, 10)), ("b", (3, 12))], eleitores, 5)
    assert r == {"votos": {"a": 2, "b": 3}, "lider": "b"}


def test_voto_dividido_sem_lider():
    eleitores = {"a": (1, 5), "b": (1, 5), "c": (1, 5), "d": (1, 5)}
    r = apurar_eleicao([("a", (1, 5)), ("c", (1, 5))], eleitores, 4)
    assert r == {"votos": {"a": 3, "c": 1}, "lider": "a"}
    r2 = apurar_eleicao([("a", (1, 5)), ("c", (1, 5))], {"a": (1, 5), "c": (1, 5)}, 4)
    assert r2["lider"] is None                               # 1 x 1 de 4: nova eleição


def test_todos_se_candidatam_ninguem_vence():
    eleitores = {"a": (5, 1), "b": (5, 1), "c": (5, 1)}
    r = apurar_eleicao([("a", (5, 1)), ("b", (5, 1)), ("c", (5, 1))], eleitores, 3)
    assert r == {"votos": {"a": 1, "b": 1, "c": 1}, "lider": None}


def test_eleitor_que_ja_votou_nao_muda_o_voto():
    eleitores = {"a": (1, 1), "b": (1, 9), "x": (1, 1), "y": (1, 1)}
    r = apurar_eleicao([("a", (1, 1)), ("b", (1, 9))], eleitores, 4)
    assert r == {"votos": {"a": 3, "b": 1}, "lider": "a"}      # x e y já tinham votado em a
