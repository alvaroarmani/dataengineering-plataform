import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import disparos  # noqa: E402

CONSUMIDORES = {
    "marketing": ["vendas", "clientes"],
    "financeiro": ["vendas"],
    "diretoria": ["vendas", "clientes", "estoque"],
}


def test_espera_todos_os_insumos():
    assert disparos(CONSUMIDORES, ["vendas", "clientes"]) == [(0, "financeiro"), (1, "marketing")]


def test_atualizacao_repetida_dispara_uma_vez():
    atual = ["vendas", "vendas", "clientes", "estoque"]
    assert disparos(CONSUMIDORES, atual) == [
        (0, "financeiro"), (1, "financeiro"), (2, "marketing"), (3, "diretoria")]


def test_controle_zera_apos_disparo():
    atual = ["clientes", "vendas", "clientes", "vendas"]
    assert [d for d in disparos(CONSUMIDORES, atual) if d[1] == "marketing"] == [(1, "marketing"), (3, "marketing")]


def test_dataset_sem_consumidor_e_dag_sem_insumo():
    assert disparos(CONSUMIDORES, ["logs"]) == []
    with pytest.raises(ValueError):
        disparos({"x": []}, ["vendas"])
