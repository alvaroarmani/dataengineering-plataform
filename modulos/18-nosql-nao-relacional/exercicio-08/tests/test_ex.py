import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import tf_idf  # noqa: E402

DOCS = [
    ("a", "dados dados dados pipeline"),
    ("b", "dados kafka streaming kafka"),
    ("c", "dados spark pipeline"),
    ("d", "dados"),
]


def test_termo_presente_em_tudo_vale_zero():
    assert tf_idf(DOCS, "dados") == []


def test_termo_raro_pesa_mais():
    assert tf_idf(DOCS, "kafka") == [("b", 0.6931)]
    assert tf_idf(DOCS, "pipeline") == [("c", 0.2310), ("a", 0.1733)]


def test_consulta_com_varios_termos():
    assert tf_idf(DOCS, "kafka pipeline dados") == [("b", 0.6931), ("c", 0.2310), ("a", 0.1733)]


def test_termo_repetido_na_consulta_e_inexistente():
    assert tf_idf(DOCS, "kafka kafka") == tf_idf(DOCS, "kafka")
    assert tf_idf(DOCS, "flink") == []
    assert tf_idf([], "kafka") == []


def test_texto_curto_ganha_de_texto_longo_com_mesmo_termo():
    docs = [("curto", "spark"), ("longo", "spark " + "outra " * 9), ("x", "nada")]
    assert [d for d, _ in tf_idf(docs, "spark")] == ["curto", "longo"]
