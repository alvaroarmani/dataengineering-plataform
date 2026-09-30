import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import copy

from solucao import esquecer_titular  # noqa: E402

TABELAS = {
    "leads_marketing": [{"cliente_id": 7, "email": "ana@x.com"}, {"cliente_id": 8, "email": "bia@y.com"}],
    "pedidos": [{"pedido": 1, "cliente_id": 7, "nome": "Ana", "endereco": "Rua A", "valor": 100.0},
                {"pedido": 2, "cliente_id": 8, "nome": "Bia", "endereco": "Rua B", "valor": 50.0},
                {"pedido": 3, "cliente_id": 7, "nome": "Ana", "valor": 30.0}],
    "notas_fiscais": [{"nf": 900, "cliente_id": 7, "cpf": "123.456.789-09", "valor": 100.0}],
}
POLITICA = {
    "leads_marketing": {"acao": "apagar"},
    "pedidos": {"acao": "anonimizar", "campos": ["nome", "endereco"]},
    "notas_fiscais": {"acao": "manter"},
}


def test_cada_tabela_com_sua_acao():
    novas, _ = esquecer_titular(TABELAS, 7, POLITICA)
    assert novas["leads_marketing"] == [{"cliente_id": 8, "email": "bia@y.com"}]
    assert novas["pedidos"] == [
        {"pedido": 1, "cliente_id": None, "nome": "***", "endereco": "***", "valor": 100.0},
        {"pedido": 2, "cliente_id": 8, "nome": "Bia", "endereco": "Rua B", "valor": 50.0},
        {"pedido": 3, "cliente_id": None, "nome": "***", "valor": 30.0}]
    assert novas["notas_fiscais"] == TABELAS["notas_fiscais"]


def test_faturamento_continua_batendo():
    novas, _ = esquecer_titular(TABELAS, 7, POLITICA)
    assert sum(p["valor"] for p in novas["pedidos"]) == 180.0


def test_relatorio_de_evidencia():
    _, rel = esquecer_titular(TABELAS, 7, POLITICA)
    assert rel == {"leads_marketing": {"acao": "apagar", "registros": 1},
                   "pedidos": {"acao": "anonimizar", "registros": 2},
                   "notas_fiscais": {"acao": "manter", "registros": 1}}


def test_nao_altera_a_entrada():
    antes = copy.deepcopy(TABELAS)
    novas, _ = esquecer_titular(TABELAS, 7, POLITICA)
    novas["notas_fiscais"][0]["valor"] = 0
    assert TABELAS == antes


def test_tabela_sem_politica_e_titular_ausente():
    with pytest.raises(ValueError):
        esquecer_titular({**TABELAS, "sac": [{"cliente_id": 7}]}, 7, POLITICA)
    _, rel = esquecer_titular(TABELAS, 999, POLITICA)
    assert all(v["registros"] == 0 for v in rel.values())
