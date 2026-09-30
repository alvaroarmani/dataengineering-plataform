import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import copy

from solucao import aplicar  # noqa: E402

LINHAS = [{"preco": 10.0, "qtd": 2, "uf": "SP"}, {"preco": 5.0, "qtd": 3, "uf": "RJ"},
          {"preco": 100.0, "qtd": 1, "uf": "SP"}]


def test_pipeline_encadeado():
    passos = [("withColumn", "receita", lambda l: l["preco"] * l["qtd"]),
              ("filter", lambda l: l["uf"] == "SP"),
              ("withColumn", "faixa", lambda l: "alta" if l["receita"] >= 50 else "baixa"),
              ("drop", "qtd")]
    assert aplicar(LINHAS, passos) == [
        {"preco": 10.0, "uf": "SP", "receita": 20.0, "faixa": "baixa"},
        {"preco": 100.0, "uf": "SP", "receita": 100.0, "faixa": "alta"}]


def test_entrada_intacta():
    antes = copy.deepcopy(LINHAS)
    aplicar(LINHAS, [("withColumn", "preco", lambda l: 0), ("drop", "uf")])
    assert LINHAS == antes


def test_sobrescrever_coluna():
    r = aplicar(LINHAS, [("withColumn", "preco", lambda l: l["preco"] * 1.1)])
    assert [round(l["preco"], 2) for l in r] == [11.0, 5.5, 110.0]


def test_coluna_removida_nao_pode_ser_usada():
    with pytest.raises(ValueError, match="passo 1"):
        aplicar(LINHAS, [("drop", "qtd"), ("withColumn", "receita", lambda l: l["preco"] * l["qtd"])])
    with pytest.raises(ValueError):
        aplicar(LINHAS, [("drop", "nao_existe")])
