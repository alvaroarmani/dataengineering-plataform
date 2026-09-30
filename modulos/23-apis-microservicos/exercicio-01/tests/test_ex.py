"""Testes do Exercício 01 (M23). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import tratar  # noqa: E402


@pytest.fixture
def estado():
    return {"pedidos": {"p2": {"id": "p2", "valor": 50}, "p1": {"id": "p1", "valor": 10.5}},
            "tokens": {"tk-leitor": {"escopos": {"ler"}},
                       "tk-app": {"escopos": {"ler", "escrever"}}}}


def req(metodo, caminho, token="tk-app", corpo=None):
    return {"metodo": metodo, "caminho": caminho, "token": token, "corpo": corpo}


def test_listar_e_ler(estado):
    assert tratar(req("GET", "/pedidos", "tk-leitor"), estado) == (
        200, {"pedidos": [{"id": "p1", "valor": 10.5}, {"id": "p2", "valor": 50}]})
    assert tratar(req("GET", "/pedidos/p2", "tk-leitor"), estado) == (200, {"id": "p2", "valor": 50})


def test_ciclo_criar_substituir_remover(estado):
    assert tratar(req("POST", "/pedidos", corpo={"id": "p3", "valor": 7}), estado) == (201, {"id": "p3", "valor": 7})
    assert tratar(req("PUT", "/pedidos/p3", corpo={"id": "p3", "valor": 9}), estado) == (200, {"id": "p3", "valor": 9})
    assert estado["pedidos"]["p3"] == {"id": "p3", "valor": 9}
    assert tratar(req("DELETE", "/pedidos/p3"), estado) == (204, None)
    assert "p3" not in estado["pedidos"]
    assert tratar(req("GET", "/pedidos/p3"), estado)[0] == 404


@pytest.mark.parametrize("r, status", [
    (req("GET", "/pedidos", token=None), 401),
    (req("GET", "/pedidos", token="tk-vazado"), 401),
    (req("GET", "/clientes"), 404),
    (req("GET", "/pedidos/p1/itens"), 404),
    (req("DELETE", "/pedidos"), 405),                           # não se apaga a coleção
    (req("POST", "/pedidos/p1", corpo={"id": "p1", "valor": 1}), 405),
    (req("POST", "/pedidos", "tk-leitor", {"id": "p9", "valor": 1}), 403),
    (req("GET", "/pedidos/p404"), 404),
    (req("POST", "/pedidos", corpo={"id": "p9"}), 400),         # falta valor
    (req("POST", "/pedidos", corpo={"id": "p9", "valor": -3}), 400),
    (req("POST", "/pedidos", corpo={"id": "p9", "valor": True}), 400),
    (req("POST", "/pedidos", corpo={"id": "", "valor": 3}), 400),
    (req("PUT", "/pedidos/p1", corpo={"id": "p2", "valor": 3}), 400),  # id do corpo ≠ URL
    (req("POST", "/pedidos", corpo={"id": "p1", "valor": 3}), 409),
])
def test_erros(estado, r, status):
    antes = {k: dict(v) for k, v in estado["pedidos"].items()}
    codigo, corpo = tratar(r, estado)
    assert codigo == status and "erro" in corpo
    assert estado["pedidos"] == antes                              # erro nunca altera o estado


def test_precedencia_entre_erros(estado):
    # sem token E rota errada: autenticação vem primeiro (não revele o que existe a quem não se identificou)
    assert tratar(req("GET", "/clientes", token=None), estado)[0] == 401
    # leitor tentando apagar pedido inexistente: falta de permissão vem antes do 404
    assert tratar(req("DELETE", "/pedidos/p404", "tk-leitor"), estado)[0] == 403
    # corpo inválido num id inexistente: o 404 vem antes do 400
    assert tratar(req("PUT", "/pedidos/p404", corpo={}), estado)[0] == 404


def test_estado_nao_vaza_por_referencia(estado):
    corpo = {"id": "p5", "valor": 5}
    _, resp = tratar(req("POST", "/pedidos", corpo=corpo), estado)
    corpo["valor"] = 999
    resp["valor"] = 888
    assert estado["pedidos"]["p5"] == {"id": "p5", "valor": 5}
