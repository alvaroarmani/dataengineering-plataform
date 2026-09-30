import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import campos_abaixo, perfil_completude  # noqa: E402

NAN = float("nan")
LOTE = [
    {"id": 1, "email": "a@x.com", "cidade": "Recife", "desconto": 0},
    {"id": 2, "email": "", "cidade": "  ", "desconto": None},
    {"id": 3, "email": None, "cidade": "Natal", "desconto": 0.0},
    {"id": 4, "cidade": NAN, "desconto": False},
]


def test_perfil_conta_os_tipos_de_ausencia():
    assert perfil_completude(LOTE, ["id", "email", "cidade", "desconto"]) == {
        "id": 1.0, "email": 0.25, "cidade": 0.5, "desconto": 0.75}


def test_zero_e_false_sao_valores_presentes():
    assert perfil_completude([{"x": 0}, {"x": False}, {"x": 0.0}], ["x"]) == {"x": 1.0}


def test_campo_que_nao_existe_em_lugar_nenhum():
    assert perfil_completude(LOTE, ["telefone"]) == {"telefone": 0.0}


def test_arredonda_em_4_casas():
    assert perfil_completude([{"x": 1}, {"x": 1}, {}], ["x"]) == {"x": 0.6667}


def test_campos_abaixo_ordena_do_pior():
    perfil = perfil_completude(LOTE, ["id", "email", "cidade", "desconto"])
    assert campos_abaixo(perfil, 0.9) == ["email", "cidade", "desconto"]
    assert campos_abaixo(perfil, 0.5) == ["email"]            # 0.5 não é MENOR que 0.5
    assert campos_abaixo({"b": 0.1, "a": 0.1}, 0.5) == ["a", "b"]


def test_lote_vazio():
    with pytest.raises(ValueError):
        perfil_completude([], ["id"])
