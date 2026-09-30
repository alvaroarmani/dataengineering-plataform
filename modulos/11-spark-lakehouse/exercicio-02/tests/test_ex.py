import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import otimizar  # noqa: E402

FONTE = ["data", "cliente_id", "preco", "qtd", "desconto", "payload"]


def test_pruning_e_pushdown():
    plano = [("filter", ["data"]),
             ("withColumn", "receita", ["preco", "qtd"]),
             ("select", ["cliente_id", "receita"])]
    assert otimizar(plano, FONTE) == {"colunas_lidas": ["cliente_id", "data", "preco", "qtd"],
                                      "filtros_empurrados": [0]}


def test_filtro_em_coluna_derivada_nao_desce():
    plano = [("withColumn", "liquido", ["preco", "desconto"]),
             ("filter", ["liquido"]),
             ("filter", ["cliente_id"]),
             ("select", ["cliente_id"])]
    r = otimizar(plano, FONTE)
    assert r["filtros_empurrados"] == [2]
    assert r["colunas_lidas"] == ["cliente_id", "desconto", "preco"]      # liquido precisa das duas


def test_sem_select_le_tudo():
    assert otimizar([("filter", ["data"])], FONTE)["colunas_lidas"] == sorted(FONTE)


def test_coluna_que_saiu_no_select():
    with pytest.raises(ValueError):
        otimizar([("select", ["data"]), ("filter", ["preco"])], FONTE)
