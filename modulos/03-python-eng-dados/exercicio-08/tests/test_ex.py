import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import resumo_por_usuario, sessionizar  # noqa: E402

# minutos desde a meia-noite; gap de 30 minutos
EVENTOS = [("ana", 600), ("ana", 605), ("bia", 700), ("ana", 612), ("ana", 700), ("ana", 605),
           ("ana", 720), ("bia", 730), ("ana", 642)]


def test_sessoes_com_desordem_e_duplicata():
    assert sessionizar(EVENTOS, 30) == {
        "ana": [(600, 642, 4), (700, 720, 2)],
        "bia": [(700, 730, 2)],                   # 30 exatos: mesma sessão
    }


def test_gap_menor_quebra_mais():
    assert sessionizar(EVENTOS, 10)["ana"] == [(600, 612, 3), (642, 642, 1), (700, 700, 1), (720, 720, 1)]


def test_resumo():
    assert resumo_por_usuario(sessionizar(EVENTOS, 30)) == {
        "ana": {"sessoes": 2, "eventos": 6, "duracao_media": 31.0},
        "bia": {"sessoes": 1, "eventos": 2, "duracao_media": 30.0}}


def test_evento_unico_e_gap_invalido():
    assert sessionizar([("x", 5)], 30) == {"x": [(5, 5, 1)]}
    assert sessionizar([], 30) == {}
    with pytest.raises(ValueError):
        sessionizar(EVENTOS, 0)
