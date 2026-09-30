"""Testes do Exercício 13 (M4). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import colunas_usadas, evita_ordenacao, melhor_indice  # noqa: E402

IDX = ["estado", "cidade", "data"]


@pytest.mark.parametrize("filtros, esperado", [
    ({"estado": "=", "cidade": "=", "data": ">="}, 3),   # prefixo completo
    ({"estado": "=", "data": "="}, 1),                   # "buraco" em cidade: data não ajuda
    ({"cidade": "=", "data": "="}, 0),                   # sem a 1ª coluna, o índice não navega
    ({"estado": "between", "cidade": "="}, 1),           # faixa na 1ª coluna para tudo
    ({"estado": "=", "cidade": "like_prefixo", "data": "="}, 2),
    ({"estado": "=", "cidade": "like_sufixo"}, 1),       # LIKE '%x' não usa a árvore
    ({"estado": "funcao"}, 0),                           # UPPER(estado) = ... também não
    ({}, 0),
])
def test_colunas_usadas(filtros, esperado):
    assert colunas_usadas(IDX, filtros) == esperado


def test_operador_desconhecido():
    with pytest.raises(ValueError):
        colunas_usadas(IDX, {"estado": "~="})


INDICES = {
    "ix_estado": ["estado"],
    "ix_estado_cidade_data": ["estado", "cidade", "data"],
    "ix_data": ["data"],
    "ix_cliente_data": ["cliente_id", "data"],
}


def test_melhor_indice_pelo_prefixo_mais_longo():
    assert melhor_indice(INDICES, {"estado": "=", "cidade": "="}) == "ix_estado_cidade_data"
    assert melhor_indice(INDICES, {"cliente_id": "=", "data": "between"}) == "ix_cliente_data"


def test_melhor_indice_desempata_pelo_menor():
    # três índices usam 1 coluna (1, 2 e 3 colunas de tamanho); o menor é mais barato de ler
    assert melhor_indice(INDICES, {"estado": "=", "cliente_id": ">"}) == "ix_estado"
    empate = {"b": ["x"], "a": ["x"]}
    assert melhor_indice(empate, {"x": "="}) == "a"


def test_sem_indice_util_e_full_scan():
    assert melhor_indice(INDICES, {"cidade": "="}) is None
    assert melhor_indice(INDICES, {"data": "funcao"}) is None


def test_evita_ordenacao():
    assert evita_ordenacao(IDX, {"estado": "="}, ["cidade", "data"]) is True
    assert evita_ordenacao(IDX, {"estado": "=", "cidade": "="}, ["data"]) is True
    assert evita_ordenacao(IDX, {}, ["estado", "cidade"]) is True       # a própria ordem do índice
    assert evita_ordenacao(IDX, {"estado": ">"}, ["cidade"]) is False   # faixa não fixa o estado
    assert evita_ordenacao(IDX, {}, ["cidade"]) is False                # pula a 1ª coluna
    assert evita_ordenacao(IDX, {"estado": "="}, ["data"]) is False     # pula cidade
    assert evita_ordenacao(IDX, {"estado": "="}, []) is True
