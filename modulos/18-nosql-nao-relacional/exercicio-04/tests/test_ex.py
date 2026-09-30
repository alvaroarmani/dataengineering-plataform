"""Testes do Exercício 04 (M18). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import distribuicao, escolher_chave, fator_skew, particao  # noqa: E402

N = 8
CANDIDATAS = [["pais"], ["cliente"], ["cliente", "dia"], ["evento_id"]]


def _eventos():
    """1.200 eventos de um app: o cliente c00 (uma conta corporativa) gera 1/3 do tráfego;
    90% dos eventos são do Brasil."""
    return [{"evento_id": i,
             "cliente": "c00" if i % 3 == 0 else f"c{i % 97:02d}",
             "dia": f"2026-03-{i % 28 + 1:02d}",
             "pais": "BR" if i % 10 else "PT"} for i in range(1200)]


@pytest.fixture(scope="module")
def eventos():
    return _eventos()


def test_particao_usa_o_hash_estavel():
    assert particao(("c00",), N) == 4
    assert particao(("c00", "2026-03-01"), N) == 6
    assert particao((7,), N) == 2


def test_distribuicao_soma_o_total(eventos):
    for chave in CANDIDATAS:
        d = distribuicao(eventos, chave, N)
        assert len(d) == N and sum(d) == 1200


@pytest.mark.parametrize("chave, contagens, skew", [
    (["pais"], [1080, 0, 0, 0, 0, 0, 120, 0], 7.2),          # baixa cardinalidade: 6 nós ociosos
    (["cliente"], [107, 99, 99, 100, 499, 98, 100, 98], 3.33),  # o cliente gigante vira hotspot
    (["cliente", "dia"], [143, 150, 156, 157, 158, 160, 135, 141], 1.07),  # "bucketing" por dia
    (["evento_id"], [149, 149, 150, 152, 150, 152, 149, 149], 1.01),
])
def test_skew_de_cada_candidata(eventos, chave, contagens, skew):
    d = distribuicao(eventos, chave, N)
    assert d == contagens and fator_skew(d) == skew


def test_fator_skew_bordas():
    assert fator_skew([5, 5, 5, 5]) == 1.0
    assert fator_skew([20, 0, 0, 0]) == 4.0
    with pytest.raises(ValueError):
        fator_skew([0, 0])
    with pytest.raises(ValueError):
        fator_skew([])


def test_escolha_respeita_a_consulta(eventos):
    # evento_id distribui melhor, mas a consulta "eventos do cliente X no dia D" não conhece o id
    assert escolher_chave(eventos, CANDIDATAS, N, ["cliente", "dia"]) == (("cliente", "dia"), 1.07)
    # se a consulta só traz o cliente, o hotspot é inevitável com estas candidatas
    assert escolher_chave(eventos, CANDIDATAS, N, ["cliente"]) == (("cliente",), 3.33)
    assert escolher_chave(eventos, CANDIDATAS, N, ["evento_id", "cliente", "dia", "pais"]) == (("evento_id",), 1.01)


def test_nenhuma_chave_elegivel(eventos):
    with pytest.raises(ValueError):
        escolher_chave(eventos, CANDIDATAS, N, ["produto"])
