import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import comparar_vetores, lww, versoes_sobreviventes  # noqa: E402


def test_lww_perde_escrita_em_silencio():
    v = [{"valor": "carrinho=[livro]", "ts": 1000, "no": "sp"},
         {"valor": "carrinho=[caneca]", "ts": 1001, "no": "rj"}]
    assert lww(v)["valor"] == "carrinho=[caneca]"        # o livro sumiu sem aviso
    empate = [{"valor": "x", "ts": 5, "no": "a"}, {"valor": "y", "ts": 5, "no": "b"}]
    assert lww(empate)["valor"] == "y"
    with pytest.raises(ValueError):
        lww([])


@pytest.mark.parametrize("a, b, rel", [
    ({"sp": 1}, {"sp": 1}, "igual"),
    ({"sp": 1}, {"sp": 2}, "antes"),
    ({"sp": 2, "rj": 1}, {"sp": 1}, "depois"),
    ({"sp": 2, "rj": 0}, {"sp": 1, "rj": 1}, "concorrente"),
    ({}, {"rj": 1}, "antes"),
])
def test_comparar_vetores(a, b, rel):
    assert comparar_vetores(a, b) == rel


def test_sobreviventes_detectam_o_conflito():
    versoes = [
        {"valor": "v1", "vetor": {"sp": 1}},
        {"valor": "livro", "vetor": {"sp": 2}},              # sucede v1 (escrita em SP)
        {"valor": "caneca", "vetor": {"sp": 1, "rj": 1}},    # sucede v1 (escrita no RJ), concorrente com "livro"
    ]
    assert versoes_sobreviventes(versoes) == ["caneca", "livro"]


def test_sem_conflito_e_duplicata():
    assert versoes_sobreviventes([{"valor": "a", "vetor": {"x": 1}}, {"valor": "b", "vetor": {"x": 2}}]) == ["b"]
    assert versoes_sobreviventes([{"valor": "a", "vetor": {"x": 1}}, {"valor": "a", "vetor": {"x": 1}}]) == ["a"]
