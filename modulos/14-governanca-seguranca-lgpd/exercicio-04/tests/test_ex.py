import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import pode_acessar  # noqa: E402

POL = {
    "usuarios": {"ana": ["analista"], "bruno": ["analista_senior"], "carla": ["admin"], "dani": ["estagiario"]},
    "papeis": {
        "leitor_base": {"permite": [("marketing.*", "ler")]},
        "analista": {"herda": ["leitor_base"], "permite": [("vendas.*", "ler")],
                     "nega": [("vendas.salarios_comissao", "*")]},
        "analista_senior": {"herda": ["analista"], "permite": [("vendas.*", "escrever")]},
        "admin": {"permite": [("vendas.*", "*"), ("rh.*", "*")]},
        "estagiario": {"herda": ["estagiario_b"]},
        "estagiario_b": {"herda": ["estagiario"], "permite": [("marketing.campanhas", "ler")]},
    },
}


def test_permissao_direta_e_curinga():
    assert pode_acessar("ana", "vendas.pedidos", "ler", POL) is True
    assert pode_acessar("ana", "vendas.pedidos", "escrever", POL) is False


def test_negacao_vence_curinga():
    assert pode_acessar("ana", "vendas.salarios_comissao", "ler", POL) is False


def test_heranca_transitiva_leva_a_negacao_junto():
    assert pode_acessar("bruno", "marketing.campanhas", "ler", POL) is True        # via analista -> leitor_base
    assert pode_acessar("bruno", "vendas.pedidos", "escrever", POL) is True
    assert pode_acessar("bruno", "vendas.salarios_comissao", "escrever", POL) is False


def test_acao_curinga_e_padrao_nao_casa_por_prefixo_solto():
    assert pode_acessar("carla", "rh.folha", "apagar", POL) is True
    assert pode_acessar("carla", "rhx.folha", "ler", POL) is False     # "rh.*" não casa "rhx."
    assert pode_acessar("carla", "marketing.campanhas", "ler", POL) is False


def test_ciclo_de_heranca_e_usuario_desconhecido():
    assert pode_acessar("dani", "marketing.campanhas", "ler", POL) is True
    assert pode_acessar("dani", "marketing.leads", "ler", POL) is False
    assert pode_acessar("zeca", "vendas.pedidos", "ler", POL) is False
