import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import analisar, buscar_frase, indexar  # noqa: E402

STOP = {"de", "o", "a", "e", "em", "para"}
DOCS = [
    (1, "Banco de dados distribuído: o café da engenharia."),
    (2, "Dados de banco? Não: banco de DADOS relacional."),
    (3, "Café, café e mais CAFÉ para o time de dados."),
    (4, "Engenharia de dados em banco colunar."),
]


def test_analise_normaliza_e_remove_stopwords():
    assert analisar("Café, café e CAFÉ!", STOP) == [(0, "cafe"), (1, "cafe"), (3, "cafe")]


def test_indice_com_posicoes():
    idx = indexar(DOCS, STOP)
    assert idx["cafe"] == {1: [5], 3: [0, 1, 4]}
    assert idx["banco"] == {1: [0], 2: [2, 4], 4: [4]}
    assert "de" not in idx


def test_frase_exige_sequencia():
    idx = indexar(DOCS, STOP)
    assert buscar_frase(idx, "banco de dados", STOP) == [1, 2]      # doc 4 tem as palavras, fora de ordem
    assert buscar_frase(idx, "dados de banco", STOP) == [2, 4]   # doc 4: "dados EM banco"


def test_frase_de_uma_palavra_e_inexistente():
    idx = indexar(DOCS, STOP)
    assert buscar_frase(idx, "CAFÉ", STOP) == [1, 3]
    assert buscar_frase(idx, "banco de café", STOP) == []
    assert buscar_frase(idx, "de o", STOP) == []
